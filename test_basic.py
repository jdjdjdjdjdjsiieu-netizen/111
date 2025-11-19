"""
Basic Test Suite - Базовое тестирование без реальных API ключей
Проверка импортов, структуры кода и базовой логики
"""

import sys
import os

# Цвета для вывода
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}")
    print(f"  {text}")
    print(f"{'='*80}{Colors.RESET}\n")


def print_test(name: str, passed: bool, message: str = ""):
    status = "✓ PASS" if passed else "✗ FAIL"
    color = Colors.GREEN if passed else Colors.RED
    print(f"{color}{status}{Colors.RESET} | {name}")
    if message:
        print(f"       └─ {message}")


def test_imports():
    """Тест 1: Проверка всех импортов"""
    print_header("ТЕСТ 1: ИМПОРТЫ И ЗАВИСИМОСТИ")
    
    passed = 0
    failed = 0
    
    modules = [
        ('telethon', 'Telethon'),
        ('fastapi', 'FastAPI'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('pydantic', 'Pydantic'),
        ('aiohttp', 'AIOHTTP'),
        ('google.generativeai', 'Google Generative AI'),
        ('groq', 'Groq'),
        ('dotenv', 'Python Dotenv'),
    ]
    
    for module, name in modules:
        try:
            __import__(module)
            print_test(f"Импорт {name}", True, f"Модуль {module} загружен")
            passed += 1
        except ImportError as e:
            print_test(f"Импорт {name}", False, str(e))
            failed += 1
    
    return passed, failed


def test_project_files():
    """Тест 2: Проверка наличия файлов проекта"""
    print_header("ТЕСТ 2: ФАЙЛЫ ПРОЕКТА")
    
    passed = 0
    failed = 0
    
    files = [
        'main.py',
        'telethon_service.py',
        'knowledge_base.py',
        'free_llm_service.py',
        'dialog_initiator.py',
        'models.py',
        'database.py',
        'config.py',
        'sender.py',
        'api_keys_guide.py',
        'setup_wizard.py',
        'setup_api.py',
        'requirements.txt',
        '.env',
    ]
    
    for file in files:
        file_path = f'/home/ubuntu/{file}'
        if os.path.exists(file_path):
            print_test(f"Файл {file}", True, "Найден")
            passed += 1
        else:
            print_test(f"Файл {file}", False, "Не найден")
            failed += 1
    
    return passed, failed


def test_module_structure():
    """Тест 3: Проверка структуры модулей"""
    print_header("ТЕСТ 3: СТРУКТУРА МОДУЛЕЙ")
    
    passed = 0
    failed = 0
    
    # Telethon Service
    try:
        from telethon_service import TelethonService
        service = TelethonService()
        
        methods = ['get_contacts', 'get_groups_and_channels', 'send_message', 
                  'send_batch_messages', 'get_message_history']
        
        for method in methods:
            if hasattr(service, method):
                print_test(f"TelethonService.{method}", True, "Метод существует")
                passed += 1
            else:
                print_test(f"TelethonService.{method}", False, "Метод не найден")
                failed += 1
    except Exception as e:
        print_test("TelethonService", False, str(e))
        failed += 5
    
    # Knowledge Base
    try:
        from knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        
        if kb.program_info:
            print_test("KnowledgeBase.program_info", True, f"Загружено {len(kb.program_info)} элементов")
            passed += 1
        else:
            print_test("KnowledgeBase.program_info", False, "Данные не загружены")
            failed += 1
        
        if kb.products:
            print_test("KnowledgeBase.products", True, f"Загружено {len(kb.products)} продуктов")
            passed += 1
        else:
            print_test("KnowledgeBase.products", False, "Продукты не загружены")
            failed += 1
    except Exception as e:
        print_test("KnowledgeBase", False, str(e))
        failed += 2
    
    # Free LLM Service
    try:
        from free_llm_service import FreeLLMService
        llm = FreeLLMService()
        
        methods = ['generate_with_gemini', 'generate_with_groq', 'generate_with_ollama', 'generate']
        
        for method in methods:
            if hasattr(llm, method):
                print_test(f"FreeLLMService.{method}", True, "Метод существует")
                passed += 1
            else:
                print_test(f"FreeLLMService.{method}", False, "Метод не найден")
                failed += 1
    except Exception as e:
        print_test("FreeLLMService", False, str(e))
        failed += 4
    
    # Dialog Initiator
    try:
        from dialog_initiator import DialogInitiator
        
        methods = ['generate_first_message', 'initiate_dialog', 'initiate_batch', 
                  'initiate_campaign', 'smart_followup']
        
        for method in methods:
            if hasattr(DialogInitiator, method):
                print_test(f"DialogInitiator.{method}", True, "Метод существует")
                passed += 1
            else:
                print_test(f"DialogInitiator.{method}", False, "Метод не найден")
                failed += 1
    except Exception as e:
        print_test("DialogInitiator", False, str(e))
        failed += 5
    
    return passed, failed


def test_api_keys_guide():
    """Тест 4: Проверка API Keys Guide"""
    print_header("ТЕСТ 4: API KEYS GUIDE")
    
    passed = 0
    failed = 0
    
    try:
        from api_keys_guide import APIKeysGuide, EnvManager
        
        # Проверка методов APIKeysGuide
        methods = [
            'get_telegram_api_credentials',
            'get_gemini_api_key',
            'get_groq_api_key',
            'get_huggingface_token',
        ]
        
        for method in methods:
            if hasattr(APIKeysGuide, method):
                result = getattr(APIKeysGuide, method)()
                if 'url' in result and 'steps' in result:
                    print_test(f"APIKeysGuide.{method}", True, "Метод работает корректно")
                    passed += 1
                else:
                    print_test(f"APIKeysGuide.{method}", False, "Некорректный результат")
                    failed += 1
            else:
                print_test(f"APIKeysGuide.{method}", False, "Метод не найден")
                failed += 1
        
        # Проверка EnvManager
        env_manager = EnvManager()
        validation = env_manager.validate()
        
        if 'required' in validation and 'optional' in validation:
            print_test("EnvManager.validate", True, "Валидация работает")
            passed += 1
        else:
            print_test("EnvManager.validate", False, "Валидация не работает")
            failed += 1
        
    except Exception as e:
        print_test("API Keys Guide", False, str(e))
        failed += 5
    
    return passed, failed


def test_setup_wizard():
    """Тест 5: Проверка Setup Wizard"""
    print_header("ТЕСТ 5: SETUP WIZARD")
    
    passed = 0
    failed = 0
    
    try:
        from setup_wizard import SetupWizard
        
        wizard = SetupWizard()
        
        methods = [
            'show_welcome',
            'show_api_guides',
            'setup_telegram_api',
            'setup_ai_apis',
            'setup_database',
            'save_configuration',
        ]
        
        for method in methods:
            if hasattr(wizard, method):
                print_test(f"SetupWizard.{method}", True, "Метод существует")
                passed += 1
            else:
                print_test(f"SetupWizard.{method}", False, "Метод не найден")
                failed += 1
        
    except Exception as e:
        print_test("Setup Wizard", False, str(e))
        failed += 6
    
    return passed, failed


def main():
    """Главная функция"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}╔════════════════════════════════════════════════════════════╗")
    print(f"║         ALFA PROJECT - BASIC TEST SUITE                     ║")
    print(f"║         Базовое тестирование без API ключей                 ║")
    print(f"╚════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    total_passed = 0
    total_failed = 0
    
    # Запуск тестов
    p, f = test_imports()
    total_passed += p
    total_failed += f
    
    p, f = test_project_files()
    total_passed += p
    total_failed += f
    
    p, f = test_module_structure()
    total_passed += p
    total_failed += f
    
    p, f = test_api_keys_guide()
    total_passed += p
    total_failed += f
    
    p, f = test_setup_wizard()
    total_passed += p
    total_failed += f
    
    # Итоговый отчет
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}")
    print(f"  ФИНАЛЬНЫЙ ОТЧЕТ")
    print(f"{'='*80}{Colors.RESET}")
    print(f"{Colors.GREEN}✓ Пройдено: {total_passed}{Colors.RESET}")
    print(f"{Colors.RED}✗ Не пройдено: {total_failed}{Colors.RESET}")
    print(f"Всего тестов: {total_passed + total_failed}\n")
    
    if total_failed == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ ВСЕ БАЗОВЫЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!{Colors.RESET}\n")
        print(f"{Colors.YELLOW}Следующий шаг: Настройте реальные API ключи через Setup Wizard{Colors.RESET}")
        print(f"{Colors.CYAN}Запустите: python setup_wizard.py{Colors.RESET}\n")
        return True
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ!{Colors.RESET}\n")
        return False


if __name__ == "__main__":
    result = main()
    sys.exit(0 if result else 1)
