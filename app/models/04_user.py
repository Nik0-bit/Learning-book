# ==========================================================
# LESSON 4: MODULE 3 - MODELS
# user.py - User Model
# 
# This file defines the structure of "users" table in the database.
# User model describes all user fields: email, username, password, role, status, etc.
# ==========================================================

# Line 1: Import uuid module for generating unique identifiers
# From where: built-in Python module
# What is this: uuid (Universally Unique Identifier) - way to generate unique IDs
# uuid4() - generates random UUID (probability of collision is practically zero)
import uuid
# Analogy: like passport number - each unique and non-repeatable

# Line 2: Import column types from SQLAlchemy
# Column - class for creating column in DB table
# String - data type "string" (text) for column
# DateTime - data type "date and time" for column
from sqlalchemy import Column, String, DateTime
# Analogy: Column = like cell in Excel table, String/DateTime = data type in cell

# Line 3: Import func function from SQLAlchemy
# func - SQL functions (NOW(), COUNT(), SUM(), etc.)
# func.now() - SQL function to get current date/time
from sqlalchemy.sql import func
# Analogy: func.now() = like Excel built-in function =NOW() - shows current time

# Line 4: Import Base from database.py (lesson 3)
# Base - base class from which all models inherit
# All models must inherit from Base to become tables in DB
from app.db.database import Base
# Why import from app.db.database: we use Base created in database.py file

# Line 5: Import constants from constants.py (lesson 2)
# USER_ROLE_USER - constant for regular user role ("user")
# USER_STATUS_ACTIVE - constant for active status ("active")
from app.core.constants import USER_ROLE_USER, USER_STATUS_ACTIVE
# Why use constants: instead of magic strings "user" and "active" we use clear constants


# Line 6: Empty line for readability


# Line 7: Definition of User class
# class User(Base): - creates User class inheriting from Base
# User - class name (Python convention - starts with capital letter)
# Base - parent class (from database.py)
# Inheriting from Base makes User a table in DB
class User(Base):
    
    # Line 8: __tablename__ - special SQLAlchemy attribute
    # Defines table name in database
    # "users" - table name (plural, SQL convention)
    __tablename__ = "users"
    # Why: SQLAlchemy by default names table "user" (singular),
    # but we want "users" (plural) - more correct for tables


    # Line 9: id - primary key of table (unique user identifier)
    # Column() - creates column in table
    # String - data type (string), because UUID is string like "550e8400-e29b-41d4-a716-446655440000"
    # primary_key=True - this is primary key (unique record identifier)
    # index=True - create index for fast search by id
    # default=lambda: str(uuid.uuid4()) - default value = generate new UUID and convert to string
    # lambda - anonymous function (function without name), executed when creating new record
    # str() - convert UUID to string
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    # Analogy: id = like student ID number - unique for each student
    # primary_key = like main identifier (no two are the same)
    # index = like alphabetical index in book - fast search

    # Line 10: email - user's email address
    # String - string data type
    # unique=True - email must be unique (cannot have two users with same email)
    # index=True - index for fast search by email (often used to find user)
    # nullable=False - field is required (cannot be empty/NULL)
    email = Column(String, unique=True, index=True, nullable=False)
    # Analogy: email = like login, must be unique
    # unique = like phone number - cannot have two identical ones

    # Line 11: username - username (nickname)
    # nullable=False - required
    # unique=True - must be unique (two users cannot have same username)
    username = Column(String, nullable=False, unique=True)
    # Analogy: username = like game nickname - unique name for each player

    # Line 12: password_hash - password hash (encrypted password)
    # nullable=False - required (cannot have no password)
    # Hash = one-way encryption (can encrypt, but cannot decrypt)
    # Only hash is stored in DB, not the password itself (security)
    password_hash = Column(String, nullable=False)
    # Analogy: password_hash = like fingerprint - can check match, but cannot recover original
    # Why hash: if someone steals DB, cannot learn user passwords


    # Line 13: role - user role (admin, user, subscriber)
    # nullable=False - required
    # default=USER_ROLE_USER - default value = regular user
    # USER_ROLE_USER - constant from constants.py (equals "user")
    role = Column(String, nullable=False, default=USER_ROLE_USER)
    # Analogy: role = like job position - determines what user can do

    # Line 14: status - user status (active, banned)
    # nullable=False - required
    # default=USER_STATUS_ACTIVE - active by default
    # USER_STATUS_ACTIVE - constant from constants.py (equals "active")
    status = Column(String, nullable=False, default=USER_STATUS_ACTIVE)
    # Analogy: status = like bank card status - active or blocked


    # Line 15: Comment - Discord binding section
    # Discord - messenger, user can link their Discord account to account in system
    
    # ---- Discord binding ----
    # Line 16: discord_id - unique user ID in Discord
    # unique=True - one Discord account can be linked to only one user
    # index=True - index for fast search
    # nullable=True - can be empty (user may not link Discord)
    discord_id = Column(String, unique=True, index=True, nullable=True)
    # Line 17: discord_username - username in Discord
    # nullable=True - optional (may not exist if Discord not linked)
    discord_username = Column(String, nullable=True)
    # Line 18: discord_avatar_url - link to user's avatar in Discord
    # URL = image address on internet
    # nullable=True - optional
    discord_avatar_url = Column(String, nullable=True)
    # Analogy: discord_* fields = like passport data - exists for those who linked Discord


    # Line 19: created_at - date and time of user record creation
    # DateTime(timezone=True) - "date and time" type with timezone awareness
    # timezone=True - store timezone information
    # server_default=func.now() - default value set by DB when creating record
    # func.now() - SQL function NOW() (current date/time)
    # server_default = value set by DB, not Python code (more reliable)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Analogy: created_at = like registration date - automatically set when creating
    # server_default = like postmark on envelope - set automatically by post office


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 4:
# ==========================================================
# 
# 1. What is UUID and why use it instead of regular numbers (1, 2, 3) for id?
#    What are advantages of UUID over auto-increment (1, 2, 3, 4...)?
#
# 2. What does primary_key=True mean and why is primary key needed?
#    Can a table have multiple primary keys?
#
# 3. What is index=True and why are indexes needed in DB?
#    Why is index created for email and discord_id, but not for username (although it's also unique)?
#
# 4. What is nullable=False and nullable=True?
#    What's the difference between required and optional fields?
#
# 5. Why store password_hash instead of password itself?
#    What is hashing and why is it one-way?
#
# 6. What does unique=True mean and what's the difference between unique and primary_key?
#    Why does email have both unique and index, but username only unique?
#
# 7. What is default in Column and when does default value trigger?
#    What's the difference between default and server_default?
#
# 8. What does lambda function mean in default=lambda: str(uuid.uuid4())?
#    Why use lambda instead of just str(uuid.uuid4())?
#
# 9. What is DateTime(timezone=True) and why is timezone=True needed?
#    What will happen if set timezone=False?
#
# 10. Why are discord_id, discord_username, discord_avatar_url fields needed?
#     Why are they nullable=True (can be empty)?
#
# ==========================================================
