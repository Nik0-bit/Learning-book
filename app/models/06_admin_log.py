# ==========================================================
# LESSON 6: MODULE 3 - MODELS
# admin_log.py - Admin Action Log Model
# 
# This file defines the structure of "admin_logs" table in the database.
# AdminLog model stores history of all administrator actions for audit and security.
# ==========================================================

# Line 1: Comment with file path (for understanding project structure)

# Line 2: Import datetime class from built-in datetime module
# From where: built-in Python module
# What is this: datetime - class for working with date and time
# datetime.utcnow() - method to get current date/time in UTC (Coordinated Universal Time)
from datetime import datetime
# Analogy: datetime = like calendar and clock together - shows date and time
# UTC = universal time for whole world (like standard time, doesn't depend on timezone)


# Line 3: Empty line for readability


# Line 4: Import column types from SQLAlchemy
# Text - data type "text" for long strings (unlimited length, unlike String)
# String - limited string (usually up to 255 characters), Text - unlimited text
from sqlalchemy import Column, String, DateTime, Text
# Analogy: String = like form field (limited), Text = like large text field (unlimited)

# Line 5: Empty line for readability

# Line 6: Import Base from database.py (lesson 3)
from app.db.database import Base


# Line 7: Empty line for readability


# Line 8: Definition of AdminLog class
# class AdminLog(Base): - creates AdminLog class inheriting from Base
# AdminLog = admin action log (record of what admin did)
# Why: for audit (who, what, when did) and security (tracking admin actions)
class AdminLog(Base):
    
    # Line 9: __tablename__ - table name in database
    # "admin_logs" - table name (plural, SQL convention)
    __tablename__ = "admin_logs"
    # Analogy: like visitor registration log - table of action records


    # Line 10: id - unique log record identifier
    # Column(String, ...) - string type column
    # primary_key=True - primary key (unique identifier)
    # index=True - index for fast search by id
    # BUT: no default - means id must be specified explicitly when creating (not generated automatically)
    # Why: usually id is generated in repository before creating record
    id = Column(String, primary_key=True, index=True)
    # Analogy: id = like log entry number - unique number for each entry


    # Line 11: action - action performed by administrator
    # String(64) - string with maximum 64 characters
    # nullable=False - required (need to know what was done)
    # Comment: examples of actions - "ban_user", "unban_user", "make_admin", "delete_user", "http_request"
    action = Column(String(64), nullable=False)          # ban_user / unban_user / make_admin / delete_user etc.
    # Analogy: action = like bank operation name - "transfer", "cash withdrawal", "card block"
    # Why limit to 64 characters: actions have standard names, don't need long strings


    # Line 12: admin_id - ID of administrator who performed the action
    # String - string (admin user UUID)
    # nullable=False - required (need to know who did it)
    admin_id = Column(String, nullable=False)            # who did it
    # Analogy: admin_id = like signature on document - who performed the action
    # Important: this can be admin ID or "anonymous" for unauthorized actions


    # Line 13: target_user_id - ID of user on whom action was performed
    # nullable=True - can be empty (not all actions relate to specific user)
    # Comment: for example, when banning user target_user_id = ID of banned user
    # But when viewing user list target_user_id = None (no specific target)
    target_user_id = Column(String, nullable=True)       # target of action (can be None)
    # Analogy: target_user_id = like transfer recipient - not always exists (e.g., when viewing list)


    # Line 14: details - additional action details
    # Text - unlimited text (can be long)
    # nullable=True - optional (not all actions require additional details)
    # Comment: can store any additional information as text
    # Example: "method=GET, path=/api/users, status=200, duration=0.0123" for HTTP requests
    details = Column(Text, nullable=True)                # any additional details
    # Analogy: details = like note on entry - additional information
    # Why Text instead of String: details can be long (JSON, descriptions, etc.)


    # Line 15: created_at - date and time of log record creation
    # DateTime - "date and time" data type
    # default=datetime.utcnow - default value = current UTC time
    # BUT: this is default (Python), not server_default (SQL), means time set in Python code
    # datetime.utcnow - function to get current UTC time
    # IMPORTANT: uses utcnow (without parentheses) - passes function that is called when creating
    # If it was utcnow() - function would be called once when loading module (incorrect)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Analogy: created_at = like timestamp on document - when entry was made
    # Why UTC: universal time for all (doesn't depend on server timezone)
    # Difference default vs server_default: default = Python code, server_default = SQL function in DB


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 6:
# ==========================================================
# 
# 1. Why is admin_logs table needed and what is audit?
#    Why is it important to log all administrator actions?
#
# 2. Why is String(64) used for action, not just String?
#    What are advantages of limiting string length?
#
# 3. Why is admin_id nullable=False, but target_user_id nullable=True?
#    Give examples of actions with target_user_id and without it.
#
# 4. What's the difference between Text and String in SQLAlchemy?
#    When to use Text, and when String?
#
# 5. What does default=datetime.utcnow (without parentheses) mean?
#    What will happen if write default=datetime.utcnow() (with parentheses)?
#
# 6. What's the difference between default (Python) and server_default (SQL)?
#    When to use each?
#
# 7. Why is there no default (automatic generation) for id?
#    How is id generated for AdminLog then?
#
# 8. What is UTC and why use it instead of local time?
#    What problems can arise if use local time?
#
# 9. Why is index needed on id if id is already primary_key?
#    Primary key automatically creates index, so why index=True?
#
# 10. What is audit in context of application security?
#     Which administrator actions must be logged?
#
# ==========================================================
