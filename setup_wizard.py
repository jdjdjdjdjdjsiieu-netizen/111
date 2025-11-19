"""
Setup Wizard - Мастер первоначальной настройки проекта
Интерактивный CLI для ввода всех необходимых переменных окружения
"""

import os
import sys
from typing import Optional
from api_keys_guide import APIKeysGuide, EnvManager

class Colors:
    """ANSI цвета для терминала"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class SetupWizard:
    """Мастер настройки проекта"""
    
    def __init__(self):
        self.env_manager = EnvManager()
        self.config = {}
    
    def print_header(self, text: str):
        """Вывести заголовок"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}")
        print(f"  {text}")
        print(f"{'='*80}{Colors.RESET}\n")
    
    def print_info(self, text: str):
        """Вывести информацию"""
        print(f"{Colors.CYAN}ℹ  {text}{Colors.RESET}")
    
    def print_success(self, text: str):
        """Вывести успех"""
        print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")
    
    def print_error(self, text: str):
        """Вывести ошибку"""
        print(f"{Colors.RED}✗ {text}{Colors.RESET}")
    
    def print_warning(self, text: str):
        """Вывести предупреждение"""
        print(f"{Colors.YELLOW}⚠  {text}{Colors.RESET}")
    
    def input_with_default(self, prompt: str, default: Optional[str] = None, 
                          required: bool = True, secret: bool = False) -> str:
        """
        Запросить ввод с возможностью использования значения по умолчанию
        
        Args:
            prompt: Текст запроса
            default: Значение по умолчанию
            required: Обязательное поле
            secret: Скрыть ввод (для паролей)
        
        Returns:
            Введенное значение
        """
        if default:
            prompt_text = f"{prompt} [{default}]: "
        else:
            prompt_text = f"{prompt}: "
        
        if required:
            prompt_text = f"{Colors.BOLD}{prompt_text}{Colors.RESET}"
        else:
            prompt_text = f"{Colors.YELLOW}{prompt_text}{Colors.RESET}"
        
        while True:
            value = input(prompt_text).strip()
            
            if not value and default:
                return default
            
            if not value and required:
                self.print_error("Это поле обязательно для заполнения!")
                continue
            
            return value if value else ""
    
    def confirm(self, prompt: str, default: bool = True) -> bool:
        """Запросить подтверждение"""
        default_text = "Y/n" if default else "y/N"
        response = input(f"{prompt} [{default_text}]: ").strip().lower()
        
        if not response:
            return default
        
        return response in ['y', 'yes', 'да', 'д']
    
    def show_welcome(self):
        """Показать приветствие"""
        self.print_header("ALFA CAMPAIGN MANAGER - SETUP WIZARD")
        print(f"{Colors.BOLD}Добро пожаловать в мастер настройки!{Colors.RESET}\n")
        print("Этот мастер поможет вам настроить все необходимые параметры")
        print("для запуска Telegram-бота для программы 'Свой в Альфе'.\n")
        
        self.print_info("Вам понадобятся:")
        print("  1. Telegram API credentials (API_ID, API_HASH)")
        print("  2. Номер телефона Telegram")
        print("  3. Хотя бы один AI API ключ (Gemini или Groq)")
        print("  4. (Опционально) Telegram Bot Token\n")
        
        if not self.confirm("Продолжить настройку?"):
            print("\nНастройка отменена.")
            sys.exit(0)
    
    def show_api_guides(self):
        """Показать руководства по получению API ключей"""
        self.print_header("РУКОВОДСТВА ПО ПОЛУЧЕНИЮ API КЛЮЧЕЙ")
        
        if self.confirm("Показать подробные инструкции по получению API ключей?", default=False):
            print()
            APIKeysGuide.print_all_guides()
            print()
            input(f"{Colors.YELLOW}Нажмите Enter для продолжения...{Colors.RESET}")
    
    def setup_telegram_api(self):
        """Настройка Telegram API"""
        self.print_header("1. TELEGRAM API CREDENTIALS")
        
        self.print_info("Получите API_ID и API_HASH на https://my.telegram.org")
        print("  1. Войдите на сайт")
        print("  2. Перейдите в 'API development tools'")
        print("  3. Создайте приложение")
        print("  4. Скопируйте API_ID и API_HASH\n")
        
        # API ID
        current_api_id = self.env_manager.get('TELEGRAM_API_ID')
        api_id = self.input_with_default(
            "Введите TELEGRAM_API_ID",
            default=current_api_id,
            required=True
        )
        self.config['TELEGRAM_API_ID'] = api_id
        
        # API Hash
        current_api_hash = self.env_manager.get('TELEGRAM_API_HASH')
        api_hash = self.input_with_default(
            "Введите TELEGRAM_API_HASH",
            default=current_api_hash,
            required=True,
            secret=True
        )
        self.config['TELEGRAM_API_HASH'] = api_hash
        
        # Phone Number
        current_phone = self.env_manager.get('TELEGRAM_PHONE_NUMBER')
        phone = self.input_with_default(
            "Введите номер телефона (формат: +79991234567)",
            default=current_phone,
            required=True
        )
        self.config['TELEGRAM_PHONE_NUMBER'] = phone
        
        self.print_success("Telegram API credentials настроены!")
    
    def setup_telegram_bot(self):
        """Настройка Telegram Bot (опционально)"""
        self.print_header("2. TELEGRAM BOT TOKEN (ОПЦИОНАЛЬНО)")
        
        self.print_info("Если у вас есть Telegram Bot Token, введите его.")
        self.print_warning("Это опционально - бот может работать через User API (Telethon)")
        print()
        
        if self.confirm("У вас есть Telegram Bot Token?", default=False):
            current_token = self.env_manager.get('TELEGRAM_BOT_TOKEN')
            token = self.input_with_default(
                "Введите TELEGRAM_BOT_TOKEN",
                default=current_token,
                required=False,
                secret=True
            )
            if token:
                self.config['TELEGRAM_BOT_TOKEN'] = token
                self.print_success("Telegram Bot Token настроен!")
        else:
            self.print_info("Пропускаем Telegram Bot Token")
    
    def setup_ai_apis(self):
        """Настройка AI API ключей"""
        self.print_header("3. AI API КЛЮЧИ")
        
        self.print_info("Необходим хотя бы один AI API ключ для работы бота")
        self.print_warning("Рекомендуется настроить оба (Gemini и Groq) для резервирования")
        print()
        
        # Gemini API
        print(f"{Colors.BOLD}Google Gemini API{Colors.RESET} (БЕСПЛАТНО, 60 req/min)")
        self.print_info("Получите ключ на https://makersuite.google.com/app/apikey")
        
        if self.confirm("Настроить Gemini API?", default=True):
            current_gemini = self.env_manager.get('GEMINI_API_KEY')
            gemini_key = self.input_with_default(
                "Введите GEMINI_API_KEY",
                default=current_gemini,
                required=False,
                secret=True
            )
            if gemini_key:
                self.config['GEMINI_API_KEY'] = gemini_key
                self.print_success("Gemini API ключ настроен!")
        
        print()
        
        # Groq API
        print(f"{Colors.BOLD}Groq API{Colors.RESET} (БЕСПЛАТНО, очень быстро)")
        self.print_info("Получите ключ на https://console.groq.com")
        
        if self.confirm("Настроить Groq API?", default=True):
            current_groq = self.env_manager.get('GROQ_API_KEY')
            groq_key = self.input_with_default(
                "Введите GROQ_API_KEY",
                default=current_groq,
                required=False,
                secret=True
            )
            if groq_key:
                self.config['GROQ_API_KEY'] = groq_key
                self.print_success("Groq API ключ настроен!")
        
        print()
        
        # Hugging Face (опционально)
        print(f"{Colors.BOLD}Hugging Face Token{Colors.RESET} (ОПЦИОНАЛЬНО)")
        
        if self.confirm("Настроить Hugging Face Token?", default=False):
            current_hf = self.env_manager.get('HUGGINGFACE_TOKEN')
            hf_token = self.input_with_default(
                "Введите HUGGINGFACE_TOKEN",
                default=current_hf,
                required=False,
                secret=True
            )
            if hf_token:
                self.config['HUGGINGFACE_TOKEN'] = hf_token
                self.print_success("Hugging Face Token настроен!")
        
        # Проверка наличия хотя бы одного AI ключа
        has_ai_key = 'GEMINI_API_KEY' in self.config or 'GROQ_API_KEY' in self.config
        
        if not has_ai_key:
            self.print_error("Необходим хотя бы один AI API ключ!")
            if self.confirm("Вернуться к настройке AI API?"):
                self.setup_ai_apis()
            else:
                self.print_warning("Продолжаем без AI API ключей (бот не сможет работать)")
    
    def setup_database(self):
        """Настройка базы данных"""
        self.print_header("4. БАЗА ДАННЫХ")
        
        self.print_info("По умолчанию используется SQLite (файловая БД)")
        
        if self.confirm("Использовать SQLite?", default=True):
            db_url = "sqlite:///./alfa.db"
            self.config['DATABASE_URL'] = db_url
            self.print_success(f"База данных: {db_url}")
        else:
            self.print_info("Введите DATABASE_URL для PostgreSQL/MySQL")
            db_url = self.input_with_default(
                "DATABASE_URL",
                default="postgresql://user:password@localhost/alfa_db",
                required=True
            )
            self.config['DATABASE_URL'] = db_url
    
    def save_configuration(self):
        """Сохранить конфигурацию"""
        self.print_header("5. СОХРАНЕНИЕ КОНФИГУРАЦИИ")
        
        # Обновить env_manager
        for key, value in self.config.items():
            self.env_manager.set(key, value)
        
        # Показать итоговую конфигурацию
        print(f"{Colors.BOLD}Итоговая конфигурация:{Colors.RESET}\n")
        
        for key, value in self.config.items():
            if 'KEY' in key or 'HASH' in key or 'TOKEN' in key:
                # Скрыть секретные данные
                masked_value = value[:8] + "..." if len(value) > 8 else "***"
                print(f"  {key} = {masked_value}")
            else:
                print(f"  {key} = {value}")
        
        print()
        
        if self.confirm("Сохранить конфигурацию в .env файл?"):
            self.env_manager.save()
            self.print_success("Конфигурация сохранена в .env файл!")
            
            # Проверить валидность
            validation = self.env_manager.validate()
            
            print()
            if validation['is_valid']:
                self.print_success("✅ Конфигурация валидна - можно запускать проект!")
            else:
                self.print_error("❌ Конфигурация невалидна")
                if not validation['has_ai_key']:
                    self.print_warning("Необходим хотя бы один AI API ключ")
        else:
            self.print_warning("Конфигурация не сохранена")
    
    def show_next_steps(self):
        """Показать следующие шаги"""
        self.print_header("СЛЕДУЮЩИЕ ШАГИ")
        
        print(f"{Colors.BOLD}Что делать дальше:{Colors.RESET}\n")
        print("1. Установите зависимости:")
        print(f"   {Colors.CYAN}pip install -r requirements.txt{Colors.RESET}\n")
        
        print("2. Запустите тесты:")
        print(f"   {Colors.CYAN}python test_suite.py{Colors.RESET}\n")
        
        print("3. Запустите backend:")
        print(f"   {Colors.CYAN}python main.py{Colors.RESET}\n")
        
        print("4. Откройте админ-панель:")
        print(f"   {Colors.CYAN}http://localhost:8000{Colors.RESET}\n")
        
        self.print_success("Настройка завершена! Удачи! 🚀")
    
    def run(self):
        """Запустить мастер настройки"""
        try:
            # Приветствие
            self.show_welcome()
            
            # Показать руководства
            self.show_api_guides()
            
            # Настройка компонентов
            self.setup_telegram_api()
            self.setup_telegram_bot()
            self.setup_ai_apis()
            self.setup_database()
            
            # Сохранение
            self.save_configuration()
            
            # Следующие шаги
            self.show_next_steps()
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Настройка прервана пользователем{Colors.RESET}")
            sys.exit(1)
        except Exception as e:
            print(f"\n\n{Colors.RED}Ошибка: {e}{Colors.RESET}")
            sys.exit(1)


if __name__ == "__main__":
    wizard = SetupWizard()
    wizard.run()
