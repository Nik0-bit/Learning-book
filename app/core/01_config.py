# ==========================================================
# LESSON 1: MODULE 1 - CORE
# config.py - Application Configuration
# 
# This file contains all application settings that
# are loaded from environment variables (.env file).
# ==========================================================

# Line 1: Import built-in Python module 'os'
# From where: this is a built-in Python library (no need to install via pip)
# What is this: module for working with the operating system
# Why: needed for working with environment variables (os.getenv)
import os
# What are environment variables: these are system/program settings,
# stored outside the code (in .env file or in OS settings)
# Comparison: like phone settings - they are separate from the phone itself


# Line 2: Import from external library pydantic_settings
# From where: this is an external library, installed via pip install pydantic-settings
# What is this: library for working with application settings
# BaseSettings - base class for creating classes with settings
# SettingsConfigDict - class for configuring how settings are configured
from pydantic_settings import BaseSettings, SettingsConfigDict
# What is pydantic: library for data validation (checking correctness)
# Comparison: like a security guard who checks your passport before entry - 
# if data is incorrect, doesn't let you in


# Line 3: Empty line for code readability (separates imports and classes)


# Line 4: Definition of Settings class
# class - Python keyword for creating a class (object template)
# Settings - name of our class (class = template for creating objects)
# BaseSettings - parent class from which our class inherits
# Inheritance: our class gets all functionality from BaseSettings
# Comparison: like a child inheriting surname from parents - gets their properties
class Settings(BaseSettings):
    
    # model_config = instructions for Settings class:
    # - Where to read settings from
    # - How to process data
    # - What to do with extra fields
    # - Whether to consider case sensitivity
    # Line 5: model_config - special field for configuring the class
    # SettingsConfigDict - configuration class from pydantic_settings
    # What it does: configures how our Settings class will work
    # SettingsConfigDict fills model_config with settings (instructions)
    model_config = SettingsConfigDict(
        # Line 6: env_file - path to file with environment variables
        # os.getenv("ENV_FILE", ".env") - gets value of ENV_FILE variable from system
        # If variable doesn't exist, uses ".env" by default (second argument)
        # What is .env file: text file with settings in KEY=VALUE format
        # Roles: os.getenv = executor (gets path), env_file = path (where it's saved), BaseSettings = reader (reads file)
        env_file=os.getenv("ENV_FILE", ".env"),
        # Line 7: extra="ignore" - ignore extra fields
        # If .env file has variables that don't exist in Settings class - ignore them
        # "ignore" = ignore, can also use "forbid" = forbid (raise error)
        extra="ignore",
        # Line 8: case_sensitive=False - case doesn't matter
        # SECRET_KEY and secret_key will be considered the same
        # True = case matters, False = doesn't matter
        case_sensitive=False,
    )
    # Comparison model_config: like instructions for a worker - 
    # "read settings from this folder, ignore extra, case doesn't matter"


    # Line 9: Comment - JWT section (JSON Web Token)
    # JWT - method for secure data transfer between client and server
    # Comparison: like a pass with information about you, checked at entry
    
    # JWT
    # Line 10: SECRET_KEY - secret key for signing JWT tokens
    # str - data type "string" (text)
    # Required field (no default value) - must be in .env file
    # Why: used for creating and verifying security tokens
    SECRET_KEY: str
    # Comparison: like a secret code for a safe - can't open/close without it
    
    # Line 11: ACCESS_TOKEN_EXPIRE_MINUTES - access token lifetime in minutes
    # int - data type "integer" (e.g.: 1, 2, 60)
    # = 60 - default value if not specified in .env
    # What is this: after how many minutes the token stops working (expires)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    # Comparison: like pass expiration date - need to get a new one after an hour


    # Line 12: Comment - documentation access key
    # Docs = documentation (Swagger UI - web interface for testing API)
    
    # Docs access key
    # Line 13: DOCS_API_KEY - secret key for accessing documentation
    # str - string (text)
    # Required field - must be in .env
    # Why: protect documentation from unauthorized access (need to know key to view)
    DOCS_API_KEY: str
    # Comparison: like Wi-Fi password - can't connect without it


    # Line 14: Comment - CORS settings
    # CORS = Cross-Origin Resource Sharing (sharing resources between origins)
    # What is this: permission for browser to access API from another domain
    
    # CORS
    # Line 15: FRONTEND_CORS_ORIGINS - which domains can access the API
    # str - string
    # "*" - default value means "allow everyone"
    # Can specify specific domains: "http://localhost:3000,https://myapp.com"
    FRONTEND_CORS_ORIGINS: str = "*"
    # Comparison: like guest list for a party - who can enter


    # Line 16: Comment - Rate Limit settings (request rate limiting)
    # Rate Limit - protection against too frequent requests (DDoS protection)
    # Comparison: like limit on number of museum entries per day
    
    # ---------- Rate Limit (new lines) ----------
    # Line 17: RATE_LIMIT_ENABLED - is request rate limiting enabled
    # bool - data type "boolean" (True or False)
    # False - disabled by default
    # Why: can temporarily disable rate limiting for debugging
    RATE_LIMIT_ENABLED: bool = False
    # Line 18: RATE_LIMIT_AUTH_PER_MINUTE - how many requests per minute allowed for /auth/*
    # int - integer
    # 20 - default value (20 requests per minute)
    # /auth/* - authorization endpoints (login, registration)
    RATE_LIMIT_AUTH_PER_MINUTE: int = 20
    # Line 19: RATE_LIMIT_DISCORD_PER_MINUTE - limit for Discord endpoints
    # 30 requests per minute by default
    RATE_LIMIT_DISCORD_PER_MINUTE: int = 30
    # Line 20: RATE_LIMIT_ADMIN_PER_MINUTE - limit for admin endpoints
    # 10 requests per minute (lower, because admin operations need more protection)
    RATE_LIMIT_ADMIN_PER_MINUTE: int = 10
    # Line 21: RATE_LIMIT_DOCS_PER_MINUTE - limit for documentation
    # 20 requests per minute
    RATE_LIMIT_DOCS_PER_MINUTE: int = 20


    # Line 22: Comment - Discord integration settings
    # Discord - messenger/platform for communities
    
    # ---------- Discord ----------
    # Line 23: DISCORD_CLIENT_ID - Discord application ID (for OAuth authorization)
    # str - string, "" - empty string by default (need to fill in .env)
    # OAuth - method of authorization through third-party service (Discord)
    DISCORD_CLIENT_ID: str = ""
    # Line 24: DISCORD_CLIENT_SECRET - Discord application secret key
    # Secret key - like password, must not be shown to anyone
    DISCORD_CLIENT_SECRET: str = ""
    # Line 25: DISCORD_REDIRECT_URI - where Discord redirects after authorization
    # Example: "http://localhost:8000/discord/callback"
    # Redirect = redirection (after authorization Discord sends user back)
    DISCORD_REDIRECT_URI: str = ""
    # Line 26: DISCORD_BOT_TOKEN - Discord bot token
    # Bot - automated program in Discord that can perform actions
    # Token - like password for bot
    DISCORD_BOT_TOKEN: str = ""
    # Line 27: DISCORD_GUILD_ID - Discord server ID (guild/community)
    # Guild = Discord server (user community)
    DISCORD_GUILD_ID: str = ""
    # Line 28: DISCORD_SUBSCRIBER_ROLE_ID - subscriber role ID in Discord
    # Role - user permissions in Discord (moderator, subscriber, etc.)
    DISCORD_SUBSCRIBER_ROLE_ID: str = ""
    # Line 29: DISCORD_REQUIRE_GUILD_MEMBERSHIP - require server membership
    # bool - True or False
    # False - by default don't require (can authorize without joining server)
    # If True - user must be a Discord server member
    DISCORD_REQUIRE_GUILD_MEMBERSHIP: bool = False


    # Line 30: Comment - list of allowed IP addresses for documentation
    # IP address - unique computer address on internet (e.g.: 192.168.1.1)
    
    # Docs IP allowlist
    # Line 31: DOCS_ALLOWED_IPS - list of IPs allowed to access documentation
    # str - string, "" - empty by default (everyone can view)
    # Format: "192.168.1.1,10.0.0.1" (multiple IPs separated by comma)
    DOCS_ALLOWED_IPS: str = ""
    # Comparison: like guest whitelist - only these people can enter


    # Line 32: Comment - payment settings
    # Payments = payments (cryptocurrency transactions)
    
    # ---------- Payments ----------
    # Line 33: ALCHEMY_ETHEREUM_URL - URL for connecting to Ethereum blockchain via Alchemy
    # Alchemy - service for working with blockchain (like internet provider for blockchain)
    # Ethereum - cryptocurrency network
    # URL - server address (e.g.: "https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY")
    ALCHEMY_ETHEREUM_URL: str = ""
    # Line 34: ALCHEMY_POLYGON_URL - URL for Polygon network
    # Polygon - another cryptocurrency network (cheaper transactions)
    ALCHEMY_POLYGON_URL: str = ""
    # Line 35: ALCHEMY_ARBITRUM_URL - URL for Arbitrum network
    # Arbitrum - Layer 2 network for Ethereum (faster and cheaper)
    ALCHEMY_ARBITRUM_URL: str = ""
    # Line 36: ALCHEMY_OPTIMISM_URL - URL for Optimism network
    # Optimism - another Layer 2 network for Ethereum
    ALCHEMY_OPTIMISM_URL: str = ""
    # Line 37: HELIUS_SOLANA_URL - URL for Solana network via Helius
    # Solana - different cryptocurrency network (not related to Ethereum)
    # Helius - service for working with Solana (analog of Alchemy for Ethereum)
    HELIUS_SOLANA_URL: str = ""
    # Line 38: PAYMENT_STRICT - strict payment verification
    # bool - True or False
    # False - by default not strict (for development)
    # True - strict verification (for production) - checks that transaction actually went through
    PAYMENT_STRICT: bool = False


    # Line 39: Comment - logging level
    
    # Logging
    # Line 40: LOG_LEVEL - log detail level
    # str - string
    # "INFO" - informational level by default
    # Options: "DEBUG" (most detailed), "INFO", "WARNING", "ERROR", "CRITICAL"
    # Logs = records of what happens in application (errors, actions, etc.)
    LOG_LEVEL: str = "INFO"
    # Comparison: like music volume level - DEBUG = very loud, ERROR = only screams


# Line 41: Empty line to separate class and code below


# Line 42: settings - create instance of Settings class
# Settings() - calling class as function creates object (class instance)
# settings - variable that stores object with settings
# What happens: pydantic automatically reads .env file and fills class fields
settings = Settings()
# Comparison: like filling out a form - you create empty form (class),
# then fill it with data from .env file (settings = Settings())


# Line 43: Comment - convenient aliases (pseudonyms)
# Alias = short name instead of long one (settings.SECRET_KEY → SECRET_KEY)

# Convenient aliases
# Line 44: SECRET_KEY - create alias variable
# settings.SECRET_KEY - access SECRET_KEY field of settings object
# SECRET_KEY = ... - create new variable with same value
# Why: can write SECRET_KEY instead of settings.SECRET_KEY (shorter)
SECRET_KEY = settings.SECRET_KEY
# Line 45: ACCESS_TOKEN_EXPIRE_MINUTES - alias for token lifetime
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Lines 46-87: similarly create aliases for all other settings
# This allows importing settings directly: from app.core.config import SECRET_KEY
# Instead of: from app.core.config import settings; key = settings.SECRET_KEY

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
# QUESTIONS FOR REINFORCING LESSON 1:
# ==========================================================
# 
# 1. What are environment variables (.env file)? 
#    Why are they needed and why don't we store secrets directly in code?
#
# 2. What is pydantic and BaseSettings? 
#    Why is pydantic-settings library needed for working with settings?
#
# 3. What does extra="ignore" mean in model_config? 
#    What will happen if we set extra="forbid"?
#
# 4. What is CORS and why is FRONTEND_CORS_ORIGINS setting needed?
#    Why can "*" be unsafe in production?
#
# 5. What is Rate Limit and why is it needed?
#    Why is limit for admin endpoints lower (10) than for auth (20)?
#
# 6. What is JWT token and why is SECRET_KEY needed?
#    What will happen if someone finds out SECRET_KEY?
#
# 7. Why create aliases at the end of file (SECRET_KEY = settings.SECRET_KEY)?
#    What advantage does this approach give?
#
# 8. What is OAuth and why are DISCORD_CLIENT_ID and DISCORD_CLIENT_SECRET needed?
#    Why should CLIENT_SECRET be kept secret?
#
# 9. What are blockchain networks (Ethereum, Polygon, Arbitrum, Optimism, Solana)?
#    Why are different URLs needed for different networks?
#
# 10. What is LOG_LEVEL and what are the logging levels?
#     When to use DEBUG, and when ERROR?
#
# ==========================================================
