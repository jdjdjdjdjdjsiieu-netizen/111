import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from openai import OpenAI
import json

from config import BOT_TOKEN, OPENAI_API_KEY, LLM_MODEL, PARTNER_LINKS, PRODUCT_INFO, CONTEXT_QUESTIONS, OBJECTION_HANDLING_PROMPT
from db import init_db, get_user_data, update_user_data, add_contact, get_all_contacts

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация базы данных
init_db()

# Инициализация клиента OpenAI
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
else:
    openai_client = None
    logging.warning("OPENAI_API_KEY не установлен. ИИ-функции будут недоступны.")

# Определение состояний для FSM
class RecommendationForm(StatesGroup):
    waiting_for_question_1 = State()
    waiting_for_question_2 = State()
    waiting_for_question_3 = State()
    waiting_for_question_4 = State()
    ready_for_recommendation = State()
    waiting_for_objection = State() # Новое состояние для обработки возражений

class ContactUpload(StatesGroup):
    waiting_for_file = State()

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- ИИ-функция для получения рекомендации ---

async def get_ai_objection_handling(objection: str, product_key: str) -> str:
    """
    Обращается к LLM для обработки возражения.
    """
    if not openai_client:
        return "Извините, ИИ-функции временно недоступны. Пожалуйста, повторите попытку позже."

    product_info = PRODUCT_INFO # Используем общую информацию о продуктах
    
    prompt = f"""
    {OBJECTION_HANDLING_PROMPT}

    **Контекст:**
    Клиент возражает после того, как ему был рекомендован продукт: {product_key}.
    Информация о продуктах: {product_info}

    **Возражение клиента:**
    "{objection}"

    Сгенерируй ответ, который отработает это возражение и вернет клиента к оформлению продукта.
    """

    try:
        response = openai_client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Отработай возражение."}
            ]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logging.error(f"Ошибка при обрабощении возражения: {e}")
        return "Извините, произошла ошибка при обработке вашего возражения. Возможно, вы хотите задать другой вопрос?"

async def get_ai_recommendation(context_data: dict) -> tuple[str, str]:
    """
    Обращается к LLM для получения персонализированной рекомендации продукта.
    Возвращает (название_продукта, текст_рекомендации).
    """
    if not openai_client:
        return "debit_card", "Извините, ИИ-функции временно недоступны. Рекомендуем начать с Дебетовой карты 'Для СВОИХ'."

    # Формирование промпта для LLM
    prompt = f"""
    Ты — высококвалифицированный финансовый консультант и партнер проекта "Свой в Альфе" от Альфа-Банка.
    Твоя задача — проанализировать данные клиента и порекомендовать ОДИН наиболее подходящий и **баллоемкий** продукт Альфа-Банка из списка.
    Цель: максимизировать потенциальный заработок партнера (владельца бота) в проекте "Свой в Альфе" при минимальном риске для клиента.

    **Стиль общения:**
    {AI_STYLE_PROMPT}
    
    **Данные о продуктах и баллах (для справке):**
    {PRODUCT_INFO}

    **Данные клиента:**
    {json.dumps(context_data, ensure_ascii=False, indent=2)}

    **Инструкции:**
    1. Проанализируй данные клиента.
    2. Выбери ОДИН продукт, который:
        а) Максимально соответствует финансовой цели клиента.
        б) Является наиболее баллоемким среди подходящих.
    3. Сгенерируй убедительный, персонализированный текст-рекомендацию (до 500 символов), **строго следуя заданному стилю общения**.
    4. Верни ответ в формате JSON с двумя полями: "product_key" (ключ из PARTNER_LINKS: debit_card, credit_card, cash_loan, partner_recruiting) и "recommendation_text".

    Пример ответа:
    {{
        "product_key": "debit_card",
        "recommendation_text": "Текст рекомендации..."
    }}
    """

    try:
        response = openai_client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Сгенерируй рекомендацию на основе предоставленных данных."}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        product_key = result.get("product_key", "debit_card")
        text = result.get("recommendation_text", "Не удалось сгенерировать текст, но рекомендуем Дебетовую карту.")
        
        return product_key, text
        
    except Exception as e:
        logging.error(f"Ошибка при обращении к OpenAI: {e}")
        return "debit_card", "Извините, произошла ошибка при подборе рекомендации. Рекомендуем Дебетовую карту 'Для СВОИХ'."

# --- Обработчики команд и FSM ---

@dp.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext) -> None:
    """Обработчик команды /start."""
    await state.clear()
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Получить рекомендацию", callback_data="start_recommendation")],
        [types.InlineKeyboardButton(text="Заработать с Альфа-Банком", callback_data="start_recruiting")]
    ])
    
    await message.answer(
        f"Привет, {message.from_user.full_name}! Я — твой ИИ-помощник в проекте 'Свой в Альфе'.\n\n"
        "Я помогу тебе подобрать наиболее выгодный продукт Альфа-Банка или расскажу, как начать зарабатывать в проекте.",
        reply_markup=keyboard
    )

@dp.message(Command("upload"))
async def command_upload_handler(message: types.Message, state: FSMContext) -> None:
    """Обработчик команды /upload для загрузки списка контактов."""
    await state.set_state(ContactUpload.waiting_for_file)
    await message.answer("Отправьте мне файл со списком контактов (например, .txt или .csv). Каждая строка должна содержать ФИО, номер телефона и/или заметку, разделенные запятыми или точкой с запятой.")

@dp.message(ContactUpload.waiting_for_file)
async def process_contact_file(message: types.Message, state: FSMContext) -> None:
    """Обработка загруженного файла с контактами."""
    await state.clear()
    
    if not message.document:
        await message.answer("Пожалуйста, отправьте файл.")
        return

    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    
    # Скачивание файла
    local_file_path = f"/tmp/{message.document.file_name}"
    await bot.download_file(file_path, local_file_path)
    
    added_count = 0
    
    try:
        with open(local_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = [p.strip() for p in line.split(';') if p.strip()]
                if not parts:
                    continue
                
                name = parts[0]
                phone = parts[1] if len(parts) > 1 else None
                note = parts[2] if len(parts) > 2 else None
                
                add_contact(name, phone, note)
                added_count += 1
        
        await message.answer(f"✅ Успешно добавлено {added_count} контактов в базу данных.")
        
    except Exception as e:
        logging.error(f"Ошибка при обработке файла контактов: {e}")
        await message.answer(f"❌ Произошла ошибка при обработке файла. Убедитесь, что формат корректен (ФИО;Телефон;Заметка).")
    
    # Удаление временного файла
    import os
    os.remove(local_file_path)

@dp.message(Command("contacts"))
async def command_contacts_handler(message: types.Message) -> None:
    """Обработчик команды /contacts для просмотра списка контактов."""
    contacts = get_all_contacts()
    
    if not contacts:
        await message.answer("Ваш список контактов пуст. Используйте команду /upload для загрузки.")
        return
        
    response = "📋 **Ваши контакты:**\n\n"
    for contact in contacts:
        contact_id, name, phone, note, status = contact
        response += f"**ID {contact_id}**: {name} (Статус: {status})\n"
        if phone:
            response += f"  📞 {phone}\n"
        if note:
            response += f"  📝 {note}\n"
        response += "---\n"
        
    await message.answer(response, parse_mode="Markdown")

@dp.callback_query(lambda c: c.data == 'start_recommendation')
async def start_recommendation_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """Начало процесса сбора данных для рекомендации."""
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(RecommendationForm.waiting_for_question_1)
    await callback_query.message.answer(CONTEXT_QUESTIONS[0])

@dp.message(RecommendationForm.waiting_for_question_1)
async def process_q1(message: types.Message, state: FSMContext):
    """Обработка ответа на вопрос 1."""
    await state.update_data(q1_age=message.text)
    await state.set_state(RecommendationForm.waiting_for_question_2)
    await message.answer(CONTEXT_QUESTIONS[1])

@dp.message(RecommendationForm.waiting_for_question_2)
async def process_q2(message: types.Message, state: FSMContext):
    """Обработка ответа на вопрос 2."""
    await state.update_data(q2_alfa_products=message.text)
    await state.set_state(RecommendationForm.waiting_for_question_3)
    await message.answer(CONTEXT_QUESTIONS[2])

@dp.message(RecommendationForm.waiting_for_question_3)
async def process_q3(message: types.Message, state: FSMContext):
    """Обработка ответа на вопрос 3."""
    await state.update_data(q3_financial_goal=message.text)
    await state.set_state(RecommendationForm.waiting_for_question_4)
    await message.answer(CONTEXT_QUESTIONS[3])

@dp.message(RecommendationForm.waiting_for_question_4)
async def process_q4(message: types.Message, state: FSMContext):
    """Обработка ответа на вопрос 4 и генерация рекомендации."""
    await state.update_data(q4_status=message.text)
    
    # Получение всех данных
    user_data = await state.get_data()
    await state.clear() # Очистка состояния после сбора данных

    await message.answer("Спасибо! Ваш запрос обрабатывается. ИИ-модуль подбирает для Вас наиболее выгодное предложение...")

    # Вызов ИИ-функции
    product_key, recommendation_text = await get_ai_recommendation(user_data)
    
    # Формирование ответа
    link = PARTNER_LINKS.get(product_key, PARTNER_LINKS["debit_card"])
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Оформить продукт по ссылке", url=link)]
    ])
    
    await message.answer(
        f"✨ **Ваша персональная рекомендация:** ✨\n\n"
        f"{recommendation_text}\n\n"
        f"👉 [Оформить продукт]({link})",
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    
    # Переход в состояние ожидания возражений (Воронка продаж)
    await state.set_state(RecommendationForm.waiting_for_objection)
    await state.update_data(last_recommended_product=product_key)
    await message.answer("Есть ли у Вас какие-либо вопросы или сомнения по поводу этой рекомендации? Я готов ответить на них и помочь Вам принять лучшее решение! 😉")

@dp.callback_query(lambda c: c.data == 'start_recruiting')
async def start_recruiting_callback(callback_query: types.CallbackQuery):
    """Обработчик для рекрутинга партнеров."""
    await bot.answer_callback_query(callback_query.id)
    
    link = PARTNER_LINKS.get("partner_recruiting", PARTNER_LINKS["debit_card"])
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Стать партнером и начать зарабатывать", url=link)]
    ])
    
    await callback_query.message.answer(
        "🚀 **Хотите зарабатывать с Альфа-Банком?**\n\n"
        "Проект 'Свой в Альфе' — это возможность построить свой доход на рекомендациях.\n"
        "Начните с регистрации и получите доступ к обучению и всем инструментам для построения команды.\n\n"
        "👉 [Регистрация в проекте]({link})",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@dp.message(RecommendationForm.waiting_for_objection)
async def process_objection(message: types.Message, state: FSMContext):
    """Обработка возражения клиента."""
    user_objection = message.text
    data = await state.get_data()
    product_key = data.get("last_recommended_product", "debit_card")
    
    await message.answer("Секундочку, я обдумываю Ваш вопрос... 🤔")
    
    # Вызов ИИ-функции для обработки возражения
    response_text = await get_ai_objection_handling(user_objection, product_key)
    
    # Повторная отправка ссылки для оформления
    link = PARTNER_LINKS.get(product_key, PARTNER_LINKS["debit_card"])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Оформить продукт по ссылке", url=link)]
    ])
    
    await message.answer(
        response_text,
        reply_markup=keyboard
    )
    
    # Остаемся в состоянии ожидания возражений для продолжения диалога
    # await state.set_state(RecommendationForm.waiting_for_objection) # Не нужно, так как мы уже в этом состоянии

# --- Запуск бота ---
async def main() -> None:
    """Основная функция запуска бота."""
    # Проверка токена
    if BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        logging.error("Пожалуйста, замените 'YOUR_TELEGRAM_BOT_TOKEN_HERE' в config.py на реальный токен.")
        return

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен вручную.")
    except Exception as e:
        logging.error(f"Критическая ошибка в main: {e}")
