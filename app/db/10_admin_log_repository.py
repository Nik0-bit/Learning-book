# ==========================================================
# LESSON 10: MODULE 5 - DB/REPOSITORIES
# admin_log_repository.py - Repository for working with admin logs in DB
# 
# This file contains AdminLogRepository class with methods for working with admin_logs table.
# Repository provides methods for creating logs and getting history of administrator actions.
# ==========================================================

# Line 1: Comment with file path

# Line 2: Import Tuple, List, Optional types from typing module
# From where: built-in Python module
# Tuple[int, List[AdminLog]] - tuple of two elements: number and list
# List[AdminLog] - list of AdminLog objects
# Optional[str] - string or None
from typing import Tuple, List, Optional
# Tuple = tuple (immutable list) - (1, 2, 3) or (total, items)

# Line 3: Empty line for readability

# Line 4: Import Session from SQLAlchemy ORM
from sqlalchemy.orm import Session

# Line 5: Empty line for readability

# Line 6: Import AdminLog model from models/admin_log.py (lesson 6)
from app.models.admin_log import AdminLog
# Line 7: Import uuid4 function from uuid module
# uuid4 - function for generating random UUID (version 4)
from uuid import uuid4
# Why: need to generate unique ID for log
# Line 8: Import datetime class from datetime module
from datetime import datetime
# Why: need to set created_at when creating log


# Line 9: Empty line for readability


# Line 10: Definition of AdminLogRepository class
class AdminLogRepository:
    # Line 11: @staticmethod decorator
    @staticmethod
    # Line 12: Definition of create method
    # create - create new admin log in DB
    # db: Session - DB session
    # *, - asterisk means all parameters after it must be passed by name only (keyword-only)
    # Why: prevents errors when passing parameters (must explicitly specify names)
    # action: str - action performed by administrator
    # admin_id: str - ID of administrator who performed action
    # target_user_id: Optional[str] = None - target user ID (can be None)
    # details: Optional[str] = None - additional details (can be None)
    # -> AdminLog - returns created AdminLog object
    def create(
        db: Session,
        *,
        action: str,
        admin_id: str,
        target_user_id: Optional[str] = None,
        details: Optional[str] = None,
    ) -> AdminLog:
        # Line 13: log - create AdminLog object
        # AdminLog() - AdminLog class constructor (create model object)
        log = AdminLog(
            # Line 14: id=str(uuid4()) - generate unique ID
            # uuid4() - function call to generate random UUID
            # str() - convert UUID to string (UUID is object, need string)
            id=str(uuid4()),
            # Line 15: action=action - pass action parameter to constructor
            action=action,
            # Line 16: admin_id=admin_id - pass administrator ID
            admin_id=admin_id,
            # Line 17: target_user_id=target_user_id - pass target ID (can be None)
            target_user_id=target_user_id,
            # Line 18: details=details - pass details (can be None)
            details=details,
            # Line 19: created_at=datetime.utcnow() - set current UTC time
            # datetime.utcnow() - function call to get current time (with parentheses!)
            # With parentheses, because we call function here (not passing function, but its result)
            created_at=datetime.utcnow(),
        )
        # AdminLog object created in Python memory, but not yet saved to DB
        
        # Line 20: db.add(log) - add log to DB session
        db.add(log)
        # Line 21: db.commit() - save to DB
        db.commit()
        # Line 22: db.refresh(log) - refresh object from DB
        db.refresh(log)
        # Line 23: return log - return created log
        return log


    # Line 24: Empty line for readability

    # Line 25: @staticmethod decorator
    @staticmethod
    # Line 26: Definition of list_logs method
    # list_logs - get list of logs with filtering and pagination
    # -> Tuple[int, List[AdminLog]] - returns tuple (total count, log list)
    # Why tuple: need to know total count for pagination (to show "page 1 of 10")
    def list_logs(
        db: Session,
        *,
        # skip: int = 0 - how many records to skip (for pagination)
        # skip = 0 means start from beginning, skip = 50 - skip first 50 records
        skip: int = 0,
        # limit: int = 50 - how many records to get (result limit)
        # limit = 50 means get maximum 50 records
        limit: int = 50,
        # action: Optional[str] = None - filter by action (optional)
        action: Optional[str] = None,
        # admin_id: Optional[str] = None - filter by administrator ID (optional)
        admin_id: Optional[str] = None,
        # target_user_id: Optional[str] = None - filter by target ID (optional)
        target_user_id: Optional[str] = None,
    ) -> Tuple[int, List[AdminLog]]:
        # Line 27: query - create base query
        # db.query(AdminLog) - query to admin_logs table
        # .order_by(AdminLog.created_at.desc()) - sort by creation date (newest to oldest)
        query = db.query(AdminLog).order_by(AdminLog.created_at.desc())
        # Initial query: all logs, sorted newest to oldest
        
        # Line 28: Empty line for readability
        
        # Line 29: if action: - check that action parameter passed (not None)
        # In Python empty string "" is considered False, but here Optional[str] can be None
        # if action checks that action is not None and not empty string
        if action:
            # Line 30: query = query.filter(...) - add filter to query
            # Filter applied only if action passed
            # query.filter() returns new query object with filter
            query = query.filter(AdminLog.action == action)
            # Now query searches only logs with specified action
        
        # Line 31: if admin_id: - check that admin_id passed
        if admin_id:
            # Line 32: Add filter by admin_id
            query = query.filter(AdminLog.admin_id == admin_id)
            # Filters accumulate (AND logic - all conditions must be met)
        
        # Line 33: if target_user_id: - check that target_user_id passed
        if target_user_id:
            # Line 34: Add filter by target_user_id
            query = query.filter(AdminLog.target_user_id == target_user_id)
        
        # Line 35: total - count total number of records (before applying skip/limit)
        # query.count() - count records matching filters
        # Called before .offset() and .limit() to get total count
        total = query.count()
        # SQL query: SELECT COUNT(*) FROM admin_logs WHERE ... (with filters)
        # Why: need to know total count for pagination (show "total 150 records")
        
        # Line 36: items - get list of logs with pagination
        # query.offset(skip) - skip first skip records
        # .limit(limit) - get maximum limit records
        # .all() - get all records (after offset and limit)
        items = query.offset(skip).limit(limit).all()
        # SQL query: SELECT * FROM admin_logs WHERE ... ORDER BY created_at DESC OFFSET ? LIMIT ?
        # offset = offset (skip first N records), limit = limit (take maximum N records)
        # Analogy: like book pages - offset = how many pages to skip, limit = how many to read
        
        # Line 37: return total, items - return tuple
        # total - total record count (for pagination)
        # items - log list for current page
        return total, items
        # Tuple (total, items) allows knowing total count and getting data


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 10:
# ==========================================================
# 
# 1. What does * mean in function parameters (after db: Session, *, action: str)?
#    Why are keyword-only arguments needed?
#
# 2. What's the difference between datetime.utcnow() (with parentheses) and datetime.utcnow (without)?
#    When to use each variant?
#
# 3. Why generate id manually (str(uuid4())) instead of using default in model?
#    What are advantages and disadvantages of each approach?
#
# 4. What is pagination and why is it needed?
#    Why not get all records at once via .all()?
#
# 5. What do skip and limit parameters mean in list_logs method?
#    How are they related to page pagination?
#
# 6. Why is total parameter needed in return value (Tuple[int, List[AdminLog]])?
#    How to use it for displaying pagination?
#
# 7. How do conditional filters work (if action: query = query.filter(...))?
#    What will happen if action = None or empty string ""?
#
# 8. What's the difference between query.count() and len(query.all())?
#    Why is count() called before offset() and limit()?
#
# 9. What are offset and limit in SQL queries?
#    How do they work together to implement pagination?
#
# 10. Why are queries built step by step (query = query.filter(...))?
#     Can one write one large query immediately?
#
# ==========================================================
