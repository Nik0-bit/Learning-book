# ==========================================================
# LESSON 16: MODULE 6 - SERVICES (Business Logic)
# admin_log_service.py - Service for working with administrator logs
# 
# This file contains the AdminLogService class for working with administrator action logs.
# The service provides methods for retrieving and filtering logs.
# ==========================================================

# Line 1: Comment with file path

# Line 2: Import types List, Dict from typing
from typing import List, Dict
# Line 3: Import Session from SQLAlchemy
from sqlalchemy.orm import Session

# Line 4: Import SessionLocal from database.py (lesson 3)
from app.db.database import SessionLocal
# Line 5: Import AdminLogRepository from admin_log_repository.py (lesson 10)
from app.db.admin_log_repository import AdminLogRepository
# Line 6: Import AdminLog model from admin_log.py (lesson 6)
from app.models.admin_log import AdminLog


# Line 7: Empty line for readability


# Line 8: Definition of AdminLogService class
class AdminLogService:
    # Line 9: @staticmethod decorator
    @staticmethod
    # Line 10: Definition of list_logs method
    # list_logs - get list of logs with filtering and pagination
    # skip: int = 0 - how many records to skip (for pagination)
    # limit: int = 50 - how many records to get (limit)
    # action: str = None - filter by action (optional)
    # admin_id: str = None - filter by administrator ID (optional)
    # target_user_id: str = None - filter by target ID (optional)
    # -> Dict - returns dictionary with total (total count) and items (list of logs)
    def list_logs(
        skip: int = 0,
        limit: int = 50,
        action: str = None,
        admin_id: str = None,
        target_user_id: str = None,
    ) -> Dict:
        # Line 11: db - create DB session
        db: Session = SessionLocal()
        # Line 12: try - start of error handling block
        try:
            # Line 13: total, items - get logs through repository
            # AdminLogRepository.list_logs() - repository method to get logs
            # Returns tuple (total, items) - total count and list of logs
            total, items = AdminLogRepository.list_logs(
                # Line 14: db - DB session
                db,
                # Line 15: skip=skip - skip records
                skip=skip,
                # Line 16: limit=limit - get records
                limit=limit,
                # Line 17: action=action - filter by action
                action=action,
                # Line 18: admin_id=admin_id - filter by admin
                admin_id=admin_id,
                # Line 19: target_user_id=target_user_id - filter by target
                target_user_id=target_user_id,
            )

            # Line 20: return - return dictionary with results
            return {
                # Line 21: "total": total - total number of records
                "total": total,
                # Line 22: "items" - list of logs converted to dictionaries
                # [AdminLogService._log_to_dict(log) for log in items] - list comprehension
                # Convert each AdminLog object to dictionary for API
                "items": [AdminLogService._log_to_dict(log) for log in items],
            }
        # Line 23: finally - block always executes
        finally:
            # Line 24: db.close() - close DB session
            db.close()

    # Line 25: @staticmethod decorator
    @staticmethod
    # Line 26: Definition of private method _log_to_dict
    # _log_to_dict - convert AdminLog object to dictionary
    # log: AdminLog - AdminLog model object
    # -> Dict - returns dictionary with log data
    def _log_to_dict(log: AdminLog) -> Dict:
        # Line 27: return - return dictionary with log data
        return {
            # Line 28: "id": log.id - log ID
            "id": log.id,
            # Line 29: "action": log.action - action
            "action": log.action,
            # Line 30: "admin_id": log.admin_id - administrator ID
            "admin_id": log.admin_id,
            # Line 31: "target_user_id": log.target_user_id - target ID (can be None)
            "target_user_id": log.target_user_id,
            # Line 32: "details": log.details - action details (can be None)
            "details": log.details,
            # Line 33: "created_at" - creation date in ISO format
            # log.created_at.isoformat() if log.created_at else None - ternary operator
            "created_at": log.created_at.isoformat() if log.created_at else None,
        }
        # Why conversion: API returns JSON (dictionaries), not Python objects


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 16:
# ==========================================================
# 
# 1. Why do we need AdminLogService if AdminLogRepository already provides methods?
#    What's the difference between service and repository?
#
# 2. What is pagination and why do we need skip and limit parameters?
#    How to use them to display logs by pages?
#
# 3. Why return total (total count) together with items (list)?
#    How is this used for pagination display in UI?
#
# 4. Why is _log_to_dict method private (with _ prefix)?
#    Can we call it from outside the class?
#
# 5. Why convert AdminLog objects to dictionaries?
#    Why doesn't API return model objects directly?
#
# 6. What does ternary operator log.created_at.isoformat() if log.created_at else None mean?
#    Why do we need if log.created_at check?
#
# 7. Why use try/finally for DB work?
#    What will happen if we don't use finally to close session?
#
# 8. How do filters (action, admin_id, target_user_id) work?
#    What will happen if we pass None as filter?
#
# 9. What's the difference between list comprehension [func(x) for x in items] and regular loop?
#    What advantages does list comprehension provide?
#
# 10. Why doesn't AdminLogService contain method for creating logs?
#     Where are logs created (which service/component)?
#
# ==========================================================

