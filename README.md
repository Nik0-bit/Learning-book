# Akiro Backend - Learning Version

## Description

This is a learning version of the Akiro Backend project with detailed comments for every line of code.

## Project Structure

The project is organized into modules with lesson numbers for sequential learning:

### Module 1 - CORE (Basic Configuration)
- `01_config.py` - Application settings
- `02_constants.py` - Constants
- `07_security.py` - JWT tokens
- `18_logger.py` - Logging
- `19_rate_limiter.py` - Rate limiting
- `20_dependencies.py` - Dependency injection
- `21_admin.py` - Admin dependencies
- `22_middleware.py` - Middleware
- `23_docs_security.py` - Documentation security

### Module 2 - DB (Database)
- `03_database.py` - Database connection
- `08_user_repository.py` - User repository
- `09_subscription_repository.py` - Subscription repository
- `10_admin_log_repository.py` - Log repository

### Module 3 - MODELS (Data Models)
- `04_user.py` - User model
- `05_subscription.py` - Subscription model
- `06_admin_log.py` - Admin log model

### Module 6 - SERVICES (Business Logic)
- `11_user_service.py` - User service
- `12_auth_service.py` - Authentication service
- `13_payment_service.py` - Payment verification service
- `14_discord_service.py` - Discord service
- `15_subscription_service.py` - Subscription service
- `16_admin_log_service.py` - Log service
- `17_cron_service.py` - Cron jobs

### Module 9 - API (Endpoints)
- `26_auth_api.py` - Authentication API
- `27_subscriptions_api.py` - Subscriptions API
- `28_discord_api.py` - Discord API
- `29_admin_api.py` - Admin API
- `30_admin_logs_api.py` - Admin logs API

### Module 10 - MAIN
- `31_main.py` - Main application file

## Features

- Every line of code has detailed comments
- Concept and term explanations
- Real-world comparisons
- Questions for review at the end of each file
- Sequential lesson structure from basic to advanced

## ⚠️ Important: Alias Files

The project has numbered files (e.g., `01_config.py`, `06_admin_log.py`) and files without numbers (e.g., `config.py`, `admin_log.py`).

**These are NOT duplicates!** These are alias files for import compatibility:

- **Numbered files** (`01_config.py`, `02_constants.py`, etc.) — learning versions with detailed comments for study
- **Files without numbers** (`config.py`, `constants.py`, etc.) — aliases that re-export from numbered files

**Why is this done?** In Python, you cannot import modules whose names begin with digits (e.g., `from app.core.01_config import ...` doesn't work directly). Therefore, alias files without numbers were created that are used in code, while numbered files are for learning.

**For learning:** read the numbered files (they contain all comments)  
**For code execution:** use files without numbers (they import from numbered files)

## Running

1. Install dependencies: `pip install -r requirements.txt`
2. Create `.env` file based on `env.sample`
3. Run server: `python run.bat` (Windows) or `python -m uvicorn app.main:app --reload`

## Learning

It is recommended to study files in order of their numbers, starting with `01_config.py` and ending with `31_main.py`.
