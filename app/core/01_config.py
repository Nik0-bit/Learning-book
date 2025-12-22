# ==========================================================
# УРОК 1: МОДУЛЬ 1 - CORE
# config.py - Конфигурация приложения
# 
# Этот файл содержит все настройки приложения, которые
# загружаются из переменных окружения (.env файл).
# ==========================================================

# Строка 1: Импорт встроенного модуля Python 'os'
# Откуда: это встроенная библиотека Python (не нужно устанавливать через pip)
# Что это: модуль для работы с операционной системой
# Зачем: нужен для работы с переменными окружения (os.getenv)
import os
# Что такое переменные окружения: это настройки системы/программы,
# которые хранятся вне кода (в файле .env или в настройках ОС)
# Сравнение: как настройки телефона - они отдельно от самого телефона


# Строка 2: Импорт из внешней библиотеки pydantic_settings
# Откуда: это внешняя библиотека, устанавливается через pip install pydantic-settings
# Что это: библиотека для работы с настройками приложения
# BaseSettings - базовый класс для создания классов с настройками
# SettingsConfigDict - класс для конфигурации того, как настраиваются настройки
from pydantic_settings import BaseSettings, SettingsConfigDict
# Что такое pydantic: библиотека для валидации данных (проверка правильности)
# Сравнение: как охранник, который проверяет паспорт перед входом - 
# если данные неверные, не пускает


# Строка 3: Пустая строка для читаемости кода (разделяет импорты и классы)


# Строка 4: Определение класса Settings
# class - ключевое слово Python для создания класса (шаблона объекта)
# Settings - название нашего класса (класс = шаблон для создания объектов)
# BaseSettings - класс-родитель, от которого наследуется наш класс
# Наследование: наш класс получает всю функциональность BaseSettings
# Сравнение: как ребёнок наследует фамилию от родителей - получает их свойства
class Settings(BaseSettings):
    
    # model_config = инструкция для класса Settings:
    # - Откуда читать настройки
    # - Как обрабатывать данные
    # - Что делать с лишним
    # - Учитывать ли регистр
    # Строка 5: model_config - специальное поле для настройки класса
    # SettingsConfigDict - класс-конфигуратор из pydantic_settings
    # Что делает: настраивает как наш класс Settings будет работать
    # SettingsConfigDict наполняет model_config настройками (инструкциями)
    model_config = SettingsConfigDict(
        # Строка 6: env_file - путь к файлу с переменными окружения
        # os.getenv("ENV_FILE", ".env") - получает значение переменной ENV_FILE из системы
        # Если переменной нет, использует ".env" по умолчанию (второй аргумент)
        # Что такое .env файл: текстовый файл с настройками в формате KEY=VALUE
        # Роли: os.getenv = исполнитель (получает путь), env_file = путь (куда сохраняется), BaseSettings = читатель (читает файл)
        env_file=os.getenv("ENV_FILE", ".env"),
        # Строка 7: extra="ignore" - игнорировать лишние поля
        # Если в .env файле есть переменные, которых нет в классе Settings - игнорировать их
        # "ignore" = игнорировать, можно также "forbid" = запрещать (выдавать ошибку)
        extra="ignore",
        # Строка 8: case_sensitive=False - регистр не важен
        # SECRET_KEY и secret_key будут считаться одинаковыми
        # True = регистр важен, False = не важен
        case_sensitive=False,
    )
    # Сравнение model_config: как инструкция для рабочего - 
    # "читай настройки из этой папки, лишнее игнорируй, регистр не важен"


    # Строка 9: Комментарий - секция JWT (JSON Web Token)
    # JWT - способ безопасной передачи данных между клиентом и сервером
    # Сравнение: как пропуск с информацией о тебе, который проверяют на входе
    
    # JWT
    # Строка 10: SECRET_KEY - секретный ключ для подписи JWT токенов
    # str - тип данных "строка" (текст)
    # Обязательное поле (нет значения по умолчанию) - должно быть в .env файле
    # Зачем: используется для создания и проверки токенов безопасности
    SECRET_KEY: str
    # Сравнение: как секретный код от сейфа - без него нельзя открыть/закрыть
    
    # Строка 11: ACCESS_TOKEN_EXPIRE_MINUTES - время жизни токена доступа в минутах
    # int - тип данных "целое число" (например: 1, 2, 60)
    # = 60 - значение по умолчанию, если не указано в .env
    # Что это: через сколько минут токен перестанет работать (истекёт)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    # Сравнение: как срок действия пропуска - через час нужно получить новый


    # Строка 12: Комментарий - ключ доступа к документации
    # Docs = документация (Swagger UI - веб-интерфейс для тестирования API)
    
    # Docs access key
    # Строка 13: DOCS_API_KEY - секретный ключ для доступа к документации
    # str - строка (текст)
    # Обязательное поле - должен быть в .env
    # Зачем: защита документации от посторонних (нужно знать ключ, чтобы посмотреть)
    DOCS_API_KEY: str
    # Сравнение: как пароль от Wi-Fi - без него не подключишься


    # Строка 14: Комментарий - CORS настройки
    # CORS = Cross-Origin Resource Sharing (совместное использование ресурсов между источниками)
    # Что это: разрешение браузеру обращаться к API с другого домена
    
    # CORS
    # Строка 15: FRONTEND_CORS_ORIGINS - какие домены могут обращаться к API
    # str - строка
    # "*" - значение по умолчанию означает "разрешить всем"
    # Можно указать конкретные домены: "http://localhost:3000,https://myapp.com"
    FRONTEND_CORS_ORIGINS: str = "*"
    # Сравнение: как список гостей на вечеринке - кто может войти


    # Строка 16: Комментарий - настройки Rate Limit (ограничение частоты запросов)
    # Rate Limit - защита от слишком частых запросов (DDoS защита)
    # Сравнение: как ограничение на количество входов в музей за день
    
    # ---------- Rate Limit (новые строки) ----------
    # Строка 17: RATE_LIMIT_ENABLED - включено ли ограничение частоты запросов
    # bool - тип данных "логический" (True или False)
    # False - по умолчанию выключено
    # Зачем: можно временно отключить rate limiting для отладки
    RATE_LIMIT_ENABLED: bool = False
    # Строка 18: RATE_LIMIT_AUTH_PER_MINUTE - сколько запросов в минуту разрешено для /auth/*
    # int - целое число
    # 20 - значение по умолчанию (20 запросов в минуту)
    # /auth/* - эндпоинты авторизации (логин, регистрация)
    RATE_LIMIT_AUTH_PER_MINUTE: int = 20
    # Строка 19: RATE_LIMIT_DISCORD_PER_MINUTE - лимит для Discord эндпоинтов
    # 30 запросов в минуту по умолчанию
    RATE_LIMIT_DISCORD_PER_MINUTE: int = 30
    # Строка 20: RATE_LIMIT_ADMIN_PER_MINUTE - лимит для админских эндпоинтов
    # 10 запросов в минуту (меньше, т.к. админские операции важнее защищать)
    RATE_LIMIT_ADMIN_PER_MINUTE: int = 10
    # Строка 21: RATE_LIMIT_DOCS_PER_MINUTE - лимит для документации
    # 20 запросов в минуту
    RATE_LIMIT_DOCS_PER_MINUTE: int = 20


    # Строка 22: Комментарий - настройки Discord интеграции
    # Discord - мессенджер/платформа для сообществ
    
    # ---------- Discord ----------
    # Строка 23: DISCORD_CLIENT_ID - ID приложения Discord (для OAuth авторизации)
    # str - строка, "" - пустая строка по умолчанию (нужно заполнить в .env)
    # OAuth - способ авторизации через сторонний сервис (Discord)
    DISCORD_CLIENT_ID: str = ""
    # Строка 24: DISCORD_CLIENT_SECRET - секретный ключ Discord приложения
    # Секретный ключ - как пароль, никому нельзя показывать
    DISCORD_CLIENT_SECRET: str = ""
    # Строка 25: DISCORD_REDIRECT_URI - куда Discord перенаправит после авторизации
    # Например: "http://localhost:8000/discord/callback"
    # Redirect = перенаправление (после авторизации Discord отправляет пользователя обратно)
    DISCORD_REDIRECT_URI: str = ""
    # Строка 26: DISCORD_BOT_TOKEN - токен Discord бота
    # Бот - автоматизированная программа в Discord, которая может выполнять действия
    # Токен - как пароль для бота
    DISCORD_BOT_TOKEN: str = ""
    # Строка 27: DISCORD_GUILD_ID - ID сервера Discord (гильдии/сообщества)
    # Guild = сервер Discord (сообщество пользователей)
    DISCORD_GUILD_ID: str = ""
    # Строка 28: DISCORD_SUBSCRIBER_ROLE_ID - ID роли подписчика в Discord
    # Роль - права пользователя в Discord (модератор, подписчик и т.д.)
    DISCORD_SUBSCRIBER_ROLE_ID: str = ""
    # Строка 29: DISCORD_REQUIRE_GUILD_MEMBERSHIP - требовать ли членство в сервере
    # bool - True или False
    # False - по умолчанию не требовать (можно авторизоваться без вступления в сервер)
    # Если True - пользователь должен быть участником Discord сервера
    DISCORD_REQUIRE_GUILD_MEMBERSHIP: bool = False


    # Строка 30: Комментарий - список разрешённых IP адресов для документации
    # IP адрес - уникальный адрес компьютера в интернете (например: 192.168.1.1)
    
    # Docs IP allowlist
    # Строка 31: DOCS_ALLOWED_IPS - список IP, которым разрешён доступ к документации
    # str - строка, "" - пустая по умолчанию (все могут смотреть)
    # Формат: "192.168.1.1,10.0.0.1" (несколько IP через запятую)
    DOCS_ALLOWED_IPS: str = ""
    # Сравнение: как белый список гостей - только эти люди могут войти


    # Строка 32: Комментарий - настройки платежей
    # Payments = платежи (криптовалютные транзакции)
    
    # ---------- Payments ----------
    # Строка 33: ALCHEMY_ETHEREUM_URL - URL для подключения к Ethereum блокчейну через Alchemy
    # Alchemy - сервис для работы с блокчейном (как провайдер интернета для блокчейна)
    # Ethereum - криптовалютная сеть
    # URL - адрес сервера (например: "https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY")
    ALCHEMY_ETHEREUM_URL: str = ""
    # Строка 34: ALCHEMY_POLYGON_URL - URL для сети Polygon
    # Polygon - ещё одна криптовалютная сеть (более дешёвые транзакции)
    ALCHEMY_POLYGON_URL: str = ""
    # Строка 35: ALCHEMY_ARBITRUM_URL - URL для сети Arbitrum
    # Arbitrum - сеть второго уровня (Layer 2) для Ethereum (быстрее и дешевле)
    ALCHEMY_ARBITRUM_URL: str = ""
    # Строка 36: ALCHEMY_OPTIMISM_URL - URL для сети Optimism
    # Optimism - ещё одна сеть Layer 2 для Ethereum
    ALCHEMY_OPTIMISM_URL: str = ""
    # Строка 37: HELIUS_SOLANA_URL - URL для сети Solana через Helius
    # Solana - другая криптовалютная сеть (не связана с Ethereum)
    # Helius - сервис для работы с Solana (аналог Alchemy для Ethereum)
    HELIUS_SOLANA_URL: str = ""
    # Строка 38: PAYMENT_STRICT - строгая проверка платежей
    # bool - True или False
    # False - по умолчанию не строгая (для разработки)
    # True - строгая проверка (для продакшена) - проверяет что транзакция реально прошла
    PAYMENT_STRICT: bool = False


    # Строка 39: Комментарий - уровень логирования
    
    # Logging
    # Строка 40: LOG_LEVEL - уровень детализации логов
    # str - строка
    # "INFO" - по умолчанию информационный уровень
    # Варианты: "DEBUG" (самый подробный), "INFO", "WARNING", "ERROR", "CRITICAL"
    # Логи = записи о том, что происходит в приложении (ошибки, действия и т.д.)
    LOG_LEVEL: str = "INFO"
    # Сравнение: как уровень громкости музыки - DEBUG = очень громко, ERROR = только крики


# Строка 41: Пустая строка для разделения класса и кода ниже


# Строка 42: settings - создание экземпляра класса Settings
# Settings() - вызов класса как функции создаёт объект (экземпляр класса)
# settings - переменная, которая хранит объект с настройками
# Что происходит: pydantic автоматически читает .env файл и заполняет поля класса
settings = Settings()
# Сравнение: как заполнение анкеты - ты создаёшь пустую анкету (класс),
# а потом заполняешь её данными из .env файла (settings = Settings())


# Строка 43: Комментарий - удобные алиасы (псевдонимы)
# Алиас = короткое имя вместо длинного (settings.SECRET_KEY → SECRET_KEY)

# Удобные алиасы
# Строка 44: SECRET_KEY - создание переменной-алиаса
# settings.SECRET_KEY - обращение к полю SECRET_KEY объекта settings
# SECRET_KEY = ... - создание новой переменной с таким же значением
# Зачем: можно писать SECRET_KEY вместо settings.SECRET_KEY (короче)
SECRET_KEY = settings.SECRET_KEY
# Строка 45: ACCESS_TOKEN_EXPIRE_MINUTES - алиас для времени жизни токена
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Строки 46-87: аналогично создаются алиасы для всех остальных настроек
# Это позволяет импортировать настройки напрямую: from app.core.config import SECRET_KEY
# Вместо: from app.core.config import settings; key = settings.SECRET_KEY

DOCS_API_KEY = settings.DOCS_API_KEY
FRONTEND_CORS_ORIGINS = settings.FRONTEND_CORS_ORIGINS

RATE_LIMIT_ENABLED = settings.RATE_LIMIT_ENABLED
RATE_LIMIT_AUTH_PER_MINUTE = settings.RATE_LIMIT_AUTH_PER_MINUTE
RATE_LIMIT_DISCORD_PER_MINUTE = settings.RATE_LIMIT_DISCORD_PER_MINUTE
RATE_LIMIT_ADMIN_PER_MINUTE = settings.RATE_LIMIT_ADMIN_PER_MINUTE
RATE_LIMIT_DOCS_PER_MINUTE = settings.RATE_LIMIT_DOCS_PER_MINUTE

DISCORD_CLIENT_ID = settings.DISCORD_CLIENT_ID
DISCORD_CLIENT_SECRET = settings.DISCORD_CLIENT_SECRET
DISCORD_REDIRECT_URI = settings.DISCORD_REDIRECT_URI
DISCORD_BOT_TOKEN = settings.DISCORD_BOT_TOKEN
DISCORD_GUILD_ID = settings.DISCORD_GUILD_ID
DISCORD_SUBSCRIBER_ROLE_ID = settings.DISCORD_SUBSCRIBER_ROLE_ID
DISCORD_REQUIRE_GUILD_MEMBERSHIP = settings.DISCORD_REQUIRE_GUILD_MEMBERSHIP

ALCHEMY_ETHEREUM_URL = settings.ALCHEMY_ETHEREUM_URL
ALCHEMY_POLYGON_URL = settings.ALCHEMY_POLYGON_URL
ALCHEMY_ARBITRUM_URL = settings.ALCHEMY_ARBITRUM_URL
ALCHEMY_OPTIMISM_URL = settings.ALCHEMY_OPTIMISM_URL
HELIUS_SOLANA_URL = settings.HELIUS_SOLANA_URL
PAYMENT_STRICT = settings.PAYMENT_STRICT
LOG_LEVEL = settings.LOG_LEVEL

DOCS_ALLOWED_IPS = settings.DOCS_ALLOWED_IPS


# ==========================================================
# ВОПРОСЫ ДЛЯ ЗАКРЕПЛЕНИЯ УРОКА 1:
# ==========================================================
# 
# 1. Что такое переменные окружения (.env файл)? 
#    Зачем они нужны и почему не храним секреты прямо в коде?
#
# 2. Что такое pydantic и BaseSettings? 
#    Зачем нужна библиотека pydantic-settings для работы с настройками?
#
# 3. Что означает extra="ignore" в model_config? 
#    Что произойдёт, если установить extra="forbid"?
#
# 4. Что такое CORS и зачем нужна настройка FRONTEND_CORS_ORIGINS?
#    Почему "*" может быть небезопасно в продакшене?
#
# 5. Что такое Rate Limit и зачем он нужен?
#    Почему для админских эндпоинтов лимит ниже (10), чем для auth (20)?
#
# 6. Что такое JWT токен и зачем нужен SECRET_KEY?
#    Что произойдёт, если кто-то узнает SECRET_KEY?
#
# 7. Зачем создавать алиасы в конце файла (SECRET_KEY = settings.SECRET_KEY)?
#    Какое преимущество даёт такой подход?
#
# 8. Что такое OAuth и зачем нужны DISCORD_CLIENT_ID и DISCORD_CLIENT_SECRET?
#    Почему CLIENT_SECRET должен храниться в секрете?
#
# 9. Что такое блокчейн-сети (Ethereum, Polygon, Arbitrum, Optimism, Solana)?
#    Зачем нужны разные URL для разных сетей?
#
# 10. Что такое LOG_LEVEL и какие бывают уровни логирования?
#     Когда использовать DEBUG, а когда ERROR?
#
# ==========================================================

