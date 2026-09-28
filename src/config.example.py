"""
Пример конфигурации QuizPlease Parser.

Скопируйте этот файл в config.py и заполните своими значениями:
    cp src/config.example.py src/config.py
"""

import os

# ============================================================
# ПУТИ ПРОЕКТА
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
SRC_DIR = os.path.join(BASE_DIR, 'src')

# ============================================================
# TELEGRAM
# ============================================================
TELEGRAM_CONFIG = {
    'token': "ВАШ_ТОКЕН_БОТА_ЗДЕСЬ",
    'chat_ids': [
        "ВАШ_CHAT_ID_ЗДЕСЬ",
        # Можно указать несколько чатов:
        # "-100XXXXXXXXXX",
    ],
    'send_test_message': False,
    'disable_notifications': False,
}

# ============================================================
# ПАРСЕР
# ============================================================
PARSER_CONFIG = {
    'base_url': "https://klg.quizplease.ru/schedule",
    'api_url': "https://api.quizplease.ru/api/games/schedule/32",  # 32 = ID города (Калуга)
    'timeout': 30,
    'user_agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    'retry_count': 3,
    'retry_delay': 2,
}

# ============================================================
# ФИЛЬТРАЦИЯ ИГР
# ============================================================
FILTER_CONFIG = {
    'game_types': ['classic', 'easy'],  # classic, easy, other
    'only_available': True,
    'exclude_reserve': True,
    'exclude_past': True,
    'future_days': 30,
}

# ============================================================
# API
# ============================================================
API_CONFIG = {
    'base_api_url': "https://api.quizplease.ru",
    'site_url': "https://klg.quizplease.ru",
    'city_id': 32,  # ID города (32 = Калуга)
    'timeout': 30,
    'max_retries': 3,
}

# ============================================================
# ЛОГИРОВАНИЕ
# ============================================================
LOGGING_CONFIG = {
    'level': 'INFO',
    'log_to_file': True,
    'log_to_console': True,
    'log_file': os.path.join(LOGS_DIR, 'quizplease.log'),
    'max_file_size': 10485760,  # 10 MB
    'backup_count': 5,
}

# ============================================================
# УВЕДОМЛЕНИЯ
# ============================================================
NOTIFICATION_CONFIG = {
    'send_telegram': True,
    'send_full_details': True,
    'only_new_games': True,
    'include_debug_info': False,
}

# ============================================================
# МОНИТОРИНГ
# ============================================================
MONITOR_CONFIG = {
    'check_interval': 900,  # 15 минут
    'max_checks': 0,        # 0 = бесконечно
    'send_summary': True,
    'send_detailed': True,
    'send_new_games_alert': True,
}

# ============================================================
# БЕЗОПАСНОСТЬ
# ============================================================
SECURITY_CONFIG = {
    'verify_ssl': False,
    'allow_redirects': True,
    'max_redirects': 5,
}

# ============================================================
# RETRY
# ============================================================
RETRY_CONFIG = {
    'max_attempts': 3,
    'base_delay': 1,
    'max_delay': 30,
    'exponential_backoff': True,
}