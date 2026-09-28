# QuizPlease Parser

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![Telegram API](https://img.shields.io/badge/Telegram%20API-✓-26A5E4?logo=telegram&logoColor=white)](https://core.telegram.org/bots/api)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-✓-2088FF?logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Systemd](https://img.shields.io/badge/Systemd-✓-DA2F47)](https://systemd.io/)

**Автоматический мониторинг расписания игр QuizPlease с уведомлениями в Telegram.**

## Задача

Площадка QuizPlease (klg.quizplease.ru) не имеет удобного способа следить за появлением новых игр. Нужно было получать уведомления, когда открывается запись на интересные форматы.

## Решение

- **Парсер через API** — работа напрямую с `api.quizplease.ru` вместо HTML-скрейпинга. Устойчиво к изменениям вёрстки, быстрее, надёжнее.
- **Telegram-уведомления** — кастомный HTTP-клиент для Bot API без тяжёлых SDK, поддержка нескольких получателей.
- **Дедупликация по хешу** — если QuizPlease меняет UUID игры, парсер не отправляет уведомление повторно. Хеш = `дата + время + название`.
- **Фильтрация по типам игр** — можно отслеживать только классические, ИЗИ, ва-банк и т.п.
- **Обработка ошибок** — таймауты, retry-логика, деградация при недоступности API.
- **Хранение истории** — текущее расписание + история изменений в JSON.
- **CI/CD** — GitHub Actions для деплоя через SSH на сервер.
- **Systemd** — работает 24/7 как сервис.

## Возможности

- Автоматический парсинг расписания игр через API
- Фильтрация по типам (classic, easy, ва-банк, новички)
- Уведомления в Telegram с деталями: дата, время, место, цена, статус
- Отслеживание изменений статуса (свободные места → резерв)
- Нахождение новых игр (дедупликация по хешу)
- Может работать как systemd-сервис

## Технологии

- **Python 3.12**
- **requests** — HTTP-клиент для API и Telegram
- **Telegram Bot API** — напрямую через HTTP
- **JSON** — хранение данных
- **systemd** — сервис для работы 24/7
- **GitHub Actions** — CI/CD

Зависимости минимальны: только `requests`, всё остальное — стандартная библиотека.

## Структура

```
quizplease-parser/
├── .github/workflows/          # CI/CD
│   ├── deploy.yml              # Деплой через SSH
│   └── fix-git.yml             # Утилита для восстановления Git
├── src/
│   ├── extract_classic_games.py # Парсер + мониторинг
│   ├── telegram_notifier.py     # Telegram-уведомления
│   ├── get_chat_id.py           # Утилита получения Chat ID
│   └── config.example.py        # Шаблон конфигурации
├── data/                        # Данные (в .gitignore)
├── logs/                        # Логи (в .gitignore)
├── requirements.txt
└── README.md
```

## Установка

```bash
git clone https://github.com/mikhailbbk/quizplease-parser.git
cd quizplease-parser

python -m venv venv
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

## Конфигурация

Скопируйте шаблон:

```bash
cp src/config.example.py src/config.py
```

Отредактируйте `src/config.py`:

```python
TELEGRAM_CONFIG = {
    'token': "ВАШ_ТОКЕН_БОТА",
    'chat_ids': ["ВАШ_CHAT_ID"],
}

PARSER_CONFIG = {
    'base_url': "https://klg.quizplease.ru/schedule",
    'api_url': "https://api.quizplease.ru/api/games/schedule/32",  # 32 = Калуга
}
```

**Как получить токен бота:**
1. Напишите `@BotFather` в Telegram
2. `/newbot`, следуйте инструкциям
3. Скопируйте токен

**Как получить Chat ID:**

```bash
python src/get_chat_id.py
```

Скрипт покажет ID чатов, которые писали боту.

## Запуск

```bash
# Локально
python src/extract_classic_games.py

# Как systemd-сервис
sudo cp deploy/quizplease.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable quizplease
sudo systemctl start quizplease
```

## Как это работает

1. **Запрос к API** — `api.quizplease.ru/api/games/schedule/32`
2. **Фильтрация** — оставляем только нужные типы игр (classic, easy)
3. **Сравнение с предыдущим состоянием** — загружаем `data/classic_games.json`, ищем новые игры и изменения статусов
4. **Дедупликация** — по хешу `дата+время+название` определяем, действительно ли игра новая
5. **Уведомление** — отправляем в Telegram только при изменениях, чтобы не спамить

## Архитектурные решения

### API вместо HTML

Изначально планировался HTML-скрейпинг через BeautifulSoup. Отказались, потому что:
- Сайт активно меняет вёрстку
- У API есть всё то же самое, но стабильнее
- Меньше зависимостей (нет `bs4`, `lxml`)

### Дедупликация по хешу

QuizPlease иногда меняет UUID игры без изменения содержимого. Наивная проверка по ID считала такую игру новой и слала уведомление повторно. Решение — проверять и по `game_hash` (хеш `дата+время+название`).

### Кастомный Telegram-клиент

Вместо `python-telegram-bot` (тяжёлый, асинхронный) — тонкая обёртка над HTTP API. Плюсы: минимум зависимостей, полный контроль, нет проблем с event loop в разных окружениях.

### Идемпотентность

Парсер не отправляет уведомления, если ничего не изменилось. Это защищает от спама при частом запуске (например, каждые 15 минут через cron или systemd timer).

## Лицензия

MIT

## Автор

**Михаил Бабков**
- GitHub: [@mikhailbbk](https://github.com/mikhailbbk)
- Telegram: [@Mikhailbbk](https://t.me/Mikhailbbk)
- Email: mikhailbbk.dev@gmail.com