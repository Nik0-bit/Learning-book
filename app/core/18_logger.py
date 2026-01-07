# ==========================================================
# LESSON 18: MODULE 7 - CORE (Additional Components)
# logger.py - Logging administrator actions
# 
# This file contains the log_action function for logging administrator actions
# to database and text file for audit and security.
# ==========================================================

# Line 1: Comment with file path

# Line 2: Import Optional type from typing
from typing import Optional
# Optional[str] = str or None (optional string)

# Line 3: Import datetime class from datetime module
from datetime import datetime
# datetime.utcnow() - get current time in UTC

# Line 4: Empty line for readability

# Line 5: Import SessionLocal from database.py (lesson 3)
from app.db.database import SessionLocal
# Line 6: Import AdminLogRepository from admin_log_repository.py (lesson 10)
from app.db.admin_log_repository import AdminLogRepository


# Line 7: Empty line for readability


# Line 8: Definition of log_action function
# log_action - function for logging administrator action
# action: str - action name (e.g., "ban_user", "subscription_paid")
# admin_id: str - administrator ID who performed action
# target_id: Optional[str] = None - target ID of action (can be None)
# details: Optional[str] = None - additional details (can be None)
# -> None - function returns nothing (only performs action)
def log_action(
    action: str,
    admin_id: str,
    target_id: Optional[str] = None,
    details: Optional[str] = None,
) -> None:
    # Line 9: Function docstring
    """
    Write admin action log to database + optionally can add log to file.
    """
    # Line 10: db - create DB session
    db = SessionLocal()
    # Line 11: try - start of error handling block
    try:
        # Line 12: AdminLogRepository.create() - create log record in DB
        AdminLogRepository.create(
            # Line 13: db - DB session
            db,
            # Line 14: action=action - action name
            action=action,
            # Line 15: admin_id=admin_id - administrator ID
            admin_id=admin_id,
            # Line 16: target_user_id=target_id - target ID of action
            target_user_id=target_id,
            # Line 17: details=details - additional details
            details=details,
        )
        # Record is saved to admin_logs table
    # Line 18: finally - block always executes (even on error)
    finally:
        # Line 19: db.close() - close DB session
        db.close()
        # Why: free connection resources

    # Line 20: Comment - additional file logging
    # Additionally can log to text file (optional)
    # Line 21: try - start of block for file writing
    try:
        # Line 22: line - form log string
        # f-string for formatting string with variable substitution
        line = f"{datetime.utcnow().isoformat()} | {action} | admin={admin_id} | target={target_id} | {details or ''}\n"
        # datetime.utcnow().isoformat() - current time in ISO format (2023-12-25T10:30:00.123456)
        # | - field separator for readability
        # {details or ''} - if details is None, use empty string
        # \n - newline character
        
        # Line 23: with open(...) - open file for writing
        # "logs.txt" - log file name
        # "a" - append mode (add to end of file, not overwrite)
        # encoding="utf-8" - UTF-8 encoding (support for non-ASCII characters)
        with open("logs.txt", "a", encoding="utf-8") as f:
            # Line 24: f.write(line) - write string to file
            f.write(line)
            # Why: additional backup of logs to file
            # Comparison: like double write - to DB (for search) and to file (for backup)
    # Line 25: except Exception - catch any errors when writing to file
    except Exception:
        # Line 26: Comment - don't crash application
        # Don't crash application due to file problems
        # pass - do nothing (ignore error)
        pass
        # Why: if couldn't write to file - not critical, log only to DB


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 18:
# ==========================================================
# 
# 1. Why do we need log_action function and what information is logged?
#    Why is it important to log administrator actions?
#
# 2. Why use try/finally for DB work?
#    What will happen if we don't use finally to close session?
#
# 3. Why duplicate logging to file and database?
#    What are advantages and disadvantages of each approach?
#
# 4. What does mode "a" mean when opening file (open("logs.txt", "a"))?
#    What's the difference between "a" (append), "w" (write) and "r" (read)?
#
# 5. Why use encoding="utf-8" when opening file?
#    What will happen if we don't specify encoding?
#
# 6. Why use pass in except Exception block?
#    Why ignore errors when writing to file?
#
# 7. What does {details or ''} mean in f-string?
#    How does or operator work with None and strings?
#
# 8. What is ISO date/time format (isoformat())?
#    Why use UTC time (utcnow()) instead of local?
#
# 9. Why do we need \n character at end of log string?
#    What will happen if we don't add newline?
#
# 10. Why does log_action function return nothing (-> None)?
#     How to handle error if logging failed?
#
# ==========================================================

