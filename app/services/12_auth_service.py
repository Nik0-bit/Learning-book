# ==========================================================
# LESSON 12: MODULE 6 - SERVICES (Business Logic)
# auth_service.py - Service for authorization and authentication
# 
# This file contains AuthService class with methods for user registration and login.
# Service handles password hashing, password verification, and JWT token creation.
# ==========================================================

# Line 1: Import Session from SQLAlchemy ORM
from sqlalchemy.orm import Session
# Line 2: Import CryptContext from passlib library
# From where: external passlib library (pip install passlib[bcrypt])
# What is this: library for working with password hashing
# CryptContext - class for configuring and using hashing algorithms
from passlib.context import CryptContext
# Analogy: CryptContext = like tool for encrypting passwords (hashing)

# Line 3: Empty line for readability

# Line 4: Import SessionLocal from database.py (lesson 3)
from app.db.database import SessionLocal
# Line 5: Import UserRepository from user_repository.py (lesson 8)
from app.db.user_repository import UserRepository
# Line 6: Import User model from models/user.py (lesson 4)
from app.models.user import User
# Line 7: Import create_access_token function from security.py (lesson 7)
from app.core.security import create_access_token
# Line 8: Import constants from constants.py (lesson 2)
from app.core.constants import USER_ROLE_USER, USER_STATUS_ACTIVE


# Line 9: Empty line for readability


# Line 10: pwd_context - create object for working with password hashing
# CryptContext() - CryptContext class constructor
# schemes=["bcrypt"] - hashing algorithm used (bcrypt - secure algorithm)
# deprecated="auto" - automatically migrate to new algorithms if old ones become deprecated
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Analogy: pwd_context = like stamp for passwords - encrypts them securely
# bcrypt = hashing algorithm specifically designed for passwords (slow, secure)


# Line 11: Empty line for readability


# Line 12: Definition of AuthService class
class AuthService:

    # Line 13: @staticmethod decorator
    @staticmethod
    # Line 14: Definition of hash_password method
    # hash_password - password hashing (one-way encryption)
    # password: str - password in plain text
    # -> str - returns password hash (encrypted string)
    def hash_password(password: str) -> str:
        # Line 15: return - return password hash
        # pwd_context.hash(password) - call hash method to create hash
        # Hash = result of one-way transformation (cannot decrypt back)
        return pwd_context.hash(password)
        # Example: password="12345" → hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYx..."

    # Line 16: @staticmethod decorator
    @staticmethod
    # Line 17: Definition of verify_password method
    # verify_password - verify password correctness
    # password: str - password in plain text (from user)
    # password_hash: str - password hash (from database)
    # -> bool - returns True if password correct, False if not
    def verify_password(password: str, password_hash: str) -> bool:
        # Line 18: return - return verification result
        # pwd_context.verify(password, password_hash) - verify password
        # verify() compares password with hash (hashes password and compares with saved hash)
        return pwd_context.verify(password, password_hash)
        # Analogy: like signature verification - compare original with reference


    # Line 19: Comment - registration section
    # -----------------------------
    #  Registration
    # -----------------------------
    # Line 20: @staticmethod decorator
    @staticmethod
    # Line 21: Definition of register_user method
    # register_user - register new user
    # email: str - user email
    # username: str - username
    # password: str - password in plain text
    # -> User - returns User object (model from DB)
    def register_user(email: str, username: str, password: str) -> User:
        # Line 22: db - create DB session
        db: Session = SessionLocal()

        # Line 23: Comment - check user existence
        # Check that user doesn't exist
        # Line 24: existing_user - check if user with this email exists
        # UserRepository.get_by_email() - search user by email through repository
        existing_user = UserRepository.get_by_email(db, email)
        # Line 25: if existing_user: - if user found (not None)
        if existing_user:
            # Line 26: db.close() - close session before exit
            db.close()
            # Line 27: raise ValueError() - raise exception
            # ValueError - built-in Python exception class for invalid values
            # "User already exists" - error message
            raise ValueError("User already exists")
            # Why: cannot create user with email that's already used

        # Line 28: existing_username - check if user with this username exists
        existing_username = UserRepository.get_by_username(db, username)
        # Line 29: if existing_username: - if username taken
        if existing_username:
            # Line 30: db.close() - close session
            db.close()
            # Line 31: raise ValueError() - raise exception
            raise ValueError("Username already taken")
            # Why: username must be unique

        # Line 32: hashed - hash password
        # AuthService.hash_password() - call static method for hashing
        hashed = AuthService.hash_password(password)
        # Important: save password hash, not password itself (security)

        # Line 33: new_user - create User object
        # User() - User model constructor (create object)
        new_user = User(
            # Line 34: email=email - set email
            email=email,
            # Line 35: username=username - set username
            username=username,
            # Line 36: password_hash=hashed - set password hash (not password itself!)
            password_hash=hashed,
        )
        # User object created in Python memory, but not yet saved to DB
        # Other fields (id, role, status, created_at) will be filled automatically (default values)

        # Line 37: saved_user - save user to DB
        # UserRepository.create() - create record in DB through repository
        saved_user = UserRepository.create(db, new_user)
        # Line 38: db.close() - close session
        db.close()

        # Line 39: return saved_user - return saved user
        return saved_user
        # saved_user contains all data from DB (including id, created_at, etc.)


    # Line 40: Comment - login section
    # -----------------------------
    #  Login
    # -----------------------------
    # Line 41: @staticmethod decorator
    @staticmethod
    # Line 42: Definition of login_user method
    # login_user - user login (authentication)
    # email: str - user email
    # password: str - password in plain text
    # -> dict - returns dictionary with user data and token
    def login_user(email: str, password: str) -> dict:
        # Line 43: db - create DB session
        db: Session = SessionLocal()

        # Line 44: user - search user by email
        user = UserRepository.get_by_email(db, email)
        # Line 45: if not user: - if user not found
        if not user:
            # Line 46: db.close() - close session
            db.close()
            # Line 47: raise ValueError() - raise exception
            raise ValueError("User not found")
            # Why: cannot login with non-existent user

        # Line 48: if not AuthService.verify_password(...) - verify password
        # verify_password() - compare entered password with hash from DB
        # user.password_hash - password hash from database
        if not AuthService.verify_password(password, user.password_hash):
            # Line 49: db.close() - close session
            db.close()
            # Line 50: raise ValueError() - raise exception
            raise ValueError("Incorrect password")
            # Why: password incorrect, access denied

        # Line 51: token - create JWT token for user
        # create_access_token() - function from security.py for creating token
        # {"user_id": user.id} - data for token (user ID)
        token = create_access_token({"user_id": user.id})
        # Token contains user ID and expiration time

        # Line 52: user_data - create dictionary with user data
        user_data = {
            # Line 53: "id": user.id - user ID
            "id": user.id,
            # Line 54: "email": user.email - email
            "email": user.email,
            # Line 55: "username": user.username - username
            "username": user.username,
            # Line 56: "created_at" - creation date in ISO format
            "created_at": user.created_at.isoformat(),
        }
        # Why: return only safe data (without password_hash)

        # Line 57: db.close() - close session
        db.close()

        # Line 58: return - return dictionary with user and token
        return {
            # Line 59: "user": user_data - user data
            "user": user_data,
            # Line 60: "token": token - JWT token for subsequent requests
            "token": token,
        }
        # Client uses token for authorized requests (in header Authorization: Bearer <token>)


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 12:
# ==========================================================
# 
# 1. What is password hashing and why is it needed?
#    Why can't passwords be stored in plain text?
#
# 2. What is bcrypt and why is it used for passwords?
#    How does bcrypt differ from regular hashing (MD5, SHA256)?
#
# 3. What does one-way encryption (hashing) mean?
#    Can password hash be decrypted back to password?
#
# 4. How does verify_password() work?
#    How to verify password if hash cannot be decrypted?
#
# 5. Why check user existence before registration?
#    What will happen if create two users with same email?
#
# 6. Why close session (db.close()) on errors (ValueError)?
#    What will happen if don't close session?
#
# 7. What is ValueError and when to use it?
#    What's the difference between ValueError and HTTPException?
#
# 8. Why is JWT token needed at login?
#    How does client use token for subsequent requests?
#
# 9. Why don't return password_hash in user_data?
#    What data is safe to return to client, and what is not?
#
# 10. What's the difference between registration (register_user) and login (login_user)?
#     What checks are performed in each case?
#
# ==========================================================
