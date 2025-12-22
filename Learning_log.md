# Learning Log - Akiro Backend Project

## Lesson 1: Configuration (`01_config.py`)

**Date:** [21.12.2025]  
**File:** `app/core/01_config.py`

### What Learned:

1. **Environment Variables (.env file)**
   - How to securely store secrets outside of code
   - Why we don't store secrets directly in code (security)
   - How `.env` file works with `os.getenv()`

2. **Pydantic and BaseSettings**
   - What pydantic is (data validation library)
   - How BaseSettings class works (reads .env automatically)
   - Inheritance from BaseSettings to create Settings class

3. **Model Configuration**
   - `model_config` as instructions for Settings class
   - `SettingsConfigDict` fills model_config with settings
   - `env_file` - path to .env file
   - `extra="ignore"` - ignore extra variables in .env
   - `case_sensitive=False` - case doesn't matter

4. **Security Settings**
   - `SECRET_KEY` - key for JWT token signing
   - `DOCS_API_KEY` - key for API documentation access
   - `DOCS_ALLOWED_IPS` - IP whitelist for documentation
   - CORS configuration (`FRONTEND_CORS_ORIGINS`)

5. **Rate Limiting (DDoS Protection)**
   - `RATE_LIMIT_ENABLED` - enable/disable rate limiting
   - Different limits for different endpoints (auth, admin, discord, docs)
   - Why admin endpoints have lower limits (security)

6. **Discord Integration**
   - OAuth authorization setup
   - `DISCORD_CLIENT_ID` - application ID (public)
   - `DISCORD_CLIENT_SECRET` - secret key (must be in .env)
   - `DISCORD_REDIRECT_URI` - callback URL after authorization
   - Bot token and role management

7. **Blockchain Integration**
   - Different RPC URLs for different networks (Ethereum, Polygon, Arbitrum, Optimism, Solana)
   - Why different URLs (different networks, different providers)
   - `PAYMENT_STRICT` - strict payment verification mode

8. **Logging**
   - `LOG_LEVEL` - controls what logs are shown in console
   - Levels: DEBUG (most detailed) → INFO → WARNING → ERROR → CRITICAL
   - When to use each level

9. **Aliases**
   - Why we create aliases (`SECRET_KEY = settings.SECRET_KEY`)
   - Makes code cleaner and easier to write
   - Easier imports: `from app.core.config import SECRET_KEY`

### Key Concepts:

- **Class vs Object**: Class is a template, object is filled with data
- **BaseSettings**: Parent class that gives ability to read .env
- **model_config**: Instructions for Settings class
- **Aliases**: Short names for convenience

### Understanding Level: **STRONG** ✅

I successfully answered all 10 questions at the end of the lesson and understood:
- How environment variables work
- How BaseSettings reads .env file
- Security concepts (CORS, Rate Limit, JWT)
- Integration setup (Discord, Blockchain)
- Code organization (aliases, configuration structure)

---

