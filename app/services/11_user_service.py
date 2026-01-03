# ==========================================================
# LESSON 11: MODULE 6 - SERVICES (Business Logic)
# user_service.py - Service for working with users
# 
# This file contains UserService class with business logic for working with users.
# Service uses UserRepository for DB work and converts models to dictionaries for API.
# ==========================================================

# Line 1: Comment with file path

# Line 2: Import Session class from SQLAlchemy ORM
from sqlalchemy.orm import Session
# Why: for typing db parameter in methods

# Line 3: Empty line for readability

# Line 4: Import SessionLocal from database.py (lesson 3)
# SessionLocal - factory for creating DB sessions
from app.db.database import SessionLocal
# Line 5: Import UserRepository from user_repository.py (lesson 8)
from app.db.user_repository import UserRepository
# Line 6: Import User model from models/user.py (lesson 4)
from app.models.user import User


# Line 7: Empty line for readability


# Line 8: Definition of UserService class
# UserService - service layer for working with users
# Service = application business logic (what it does, not how it stores data)
# Difference from repository: repository works with DB, service - with business logic
class UserService:
    # Analogy: Repository = warehouse (stores data), Service = manager (decides what to do with data)


    # Line 9: Empty line for readability
    
    # Line 10: @staticmethod decorator
    @staticmethod
    # Line 11: Definition of private method _user_to_dict
    # _user_to_dict - convert User object to dictionary (dict)
    # Prefix _ means method is private (internal, not for external use)
    # user: User - User model object (from DB)
    # -> dict - returns dictionary with user data
    def _user_to_dict(user: User) -> dict:
        # Line 12: role - get user role
        # getattr(user, "role", "user") - get "role" attribute from user object
        # If attribute doesn't exist, return "user" as default (third parameter)
        # getattr = safe attribute retrieval (won't crash if attribute missing)
        role = getattr(user, "role", "user")
        # Line 13: status - get user status similarly
        status = getattr(user, "status", "active")
        # Why getattr: protection from errors if object doesn't have attribute
        
        # Line 14: is_superadmin - check if user is superadmin
        # role == "superadmin" - compare role with "superadmin" string
        # Result: True if superadmin, False if not
        is_superadmin = role == "superadmin"
        # Line 15: is_admin - check if user is admin
        # role in ("admin", "superadmin") - check if role is in tuple
        # in - membership operator (is element in collection)
        # Superadmin is also considered admin (has admin rights and more)
        is_admin = role in ("admin", "superadmin")
        # Why: convenient boolean flags for checking access rights
        
        # Line 16: return - return dictionary with user data
        return {
            # Line 17: "id": user.id - user ID
            "id": user.id,
            # Line 18: "email": user.email - user email
            "email": user.email,
            # Line 19: "username": user.username - username
            "username": user.username,
            # Line 20: "created_at" - creation date in ISO format
            # user.created_at.isoformat() - convert date to ISO format string (2023-12-25T10:30:00)
            # if user.created_at else None - if created_at exists, convert, else None
            # Ternary operator: value1 if condition else value2
            "created_at": user.created_at.isoformat() if user.created_at else None,
            # Line 21: "role": role - user role
            "role": role,
            # Line 22: "status": status - user status
            "status": status,
            # Line 23: "discord_id" - Discord ID (optional)
            # getattr(user, "discord_id", None) - safe retrieval, if missing - None
            "discord_id": getattr(user, "discord_id", None),
            # Line 24: "discord_username" - Discord username
            "discord_username": getattr(user, "discord_username", None),
            # Line 25: "discord_avatar_url" - Discord avatar URL
            "discord_avatar_url": getattr(user, "discord_avatar_url", None),
            # Line 26: "is_admin": is_admin - flag if admin
            "is_admin": is_admin,
            # Line 27: "is_superadmin": is_superadmin - flag if superadmin
            "is_superadmin": is_superadmin,
        }
        # Why dictionary: API returns JSON (dictionaries), not Python objects


    # Line 28: Comment - data retrieval section
    # ---------- Retrieval ----------

    # Line 29: @staticmethod decorator
    @staticmethod
    # Line 30: Definition of get_user_by_id method
    # get_user_by_id - get user by ID
    # user_id: str - user ID
    # -> dict | None - returns dictionary or None (if not found)
    # dict | None - new Python 3.10+ syntax (equivalent to Optional[dict])
    def get_user_by_id(user_id: str) -> dict | None:
        # Line 31: db - create DB session
        # SessionLocal() - call factory to create new session
        # db: Session - type annotation (variable db has type Session)
        db: Session = SessionLocal()
        # Analogy: like opening book - open session, work, close
        
        # Line 32: user - get user through repository
        # UserRepository.get_by_id() - repository static method
        # db - pass DB session
        # user_id - user ID to search for
        user = UserRepository.get_by_id(db, user_id)
        # Line 33: db.close() - close DB session
        # close() - method to close DB connection
        # Important: always close session after use (free resources)
        db.close()
        # Analogy: like closing book after reading - free resources

        # Line 34: if not user: - check that user not found
        # not user - if user equals None or False
        if not user:
            # Line 35: return None - return None if user not found
            return None

        # Line 36: return - convert and return user
        # UserService._user_to_dict(user) - call private method for conversion
        # Return dictionary instead of User object
        return UserService._user_to_dict(user)


    # Line 37: @staticmethod decorator
    @staticmethod
    # Line 38: Definition of get_all_users method
    # get_all_users - get all users
    # Returns list of dictionaries (not User objects)
    def get_all_users():
        # Line 39: db - create DB session
        db: Session = SessionLocal()
        # Line 40: users - get all users through repository
        users = UserRepository.get_all(db)
        # Line 41: db.close() - close session
        db.close()

        # Line 42: return - return list of dictionaries
        # [UserService._user_to_dict(user) for user in users] - list comprehension (list generator)
        # for user in users - iterate each user in users list
        # UserService._user_to_dict(user) - convert each user to dictionary
        # Result: list of dictionaries instead of list of User objects
        return [UserService._user_to_dict(user) for user in users]
        # Analogy: like converting all documents to PDF - convert each element


    # Line 43: Comment - admin actions section
    # ---------- Admin Actions ----------

    # Line 44: @staticmethod decorator
    @staticmethod
    # Line 45: Definition of ban_user method
    # ban_user - ban (block) user
    # user_id: str - user ID to ban
    # -> bool - returns True if successful, False if user not found
    def ban_user(user_id: str) -> bool:
        # Line 46: db - create DB session
        db: Session = SessionLocal()
        # Line 47: user - get user by ID
        user = UserRepository.get_by_id(db, user_id)
        # Line 48: if not user: - check that user not found
        if not user:
            # Line 49: db.close() - close session before exit
            db.close()
            # Line 50: return False - return False (user not found)
            return False

        # Line 51: user.status = "banned" - change user status
        # Change object attribute directly (in Python memory)
        user.status = "banned"
        # Line 52: db.commit() - save changes to DB
        db.commit()
        # Line 53: db.refresh(user) - refresh object from DB
        db.refresh(user)
        # Line 54: db.close() - close session
        db.close()
        # Line 55: return True - return True (operation successful)
        return True


    # Line 56: @staticmethod decorator
    @staticmethod
    # Line 57: Definition of unban_user method
    # unban_user - unban user (remove ban)
    def unban_user(user_id: str) -> bool:
        # Line 58: db - create session
        db: Session = SessionLocal()
        # Line 59: user - get user
        user = UserRepository.get_by_id(db, user_id)
        # Line 60: if not user: - check existence
        if not user:
            # Line 61: db.close() - close session
            db.close()
            # Line 62: return False - user not found
            return False

        # Line 63: user.status = "active" - change status to active
        user.status = "active"
        # Line 64: db.commit() - save changes
        db.commit()
        # Line 65: db.refresh(user) - refresh object
        db.refresh(user)
        # Line 66: db.close() - close session
        db.close()
        # Line 67: return True - successful
        return True


    # Line 68: @staticmethod decorator
    @staticmethod
    # Line 69: Definition of make_admin method
    # make_admin - make user administrator
    def make_admin(user_id: str) -> bool:
        # Line 70: Function docstring
        """
        Makes user regular admin (NOT super).
        Used from admin panel.
        """
        # Line 71: db - create session
        db: Session = SessionLocal()
        # Line 72: user - get user
        user = UserRepository.get_by_id(db, user_id)
        # Line 73: if not user: - check existence
        if not user:
            # Line 74: db.close() - close
            db.close()
            # Line 75: return False - not found
            return False

        # Line 76: user.role = "admin" - set admin role
        # "admin" - regular admin (not superadmin)
        user.role = "admin"
        # Line 77: db.commit() - save
        db.commit()
        # Line 78: db.refresh(user) - refresh
        db.refresh(user)
        # Line 79: db.close() - close
        db.close()
        # Line 80: return True - successful
        return True


    # Line 81: @staticmethod decorator
    @staticmethod
    # Line 82: Definition of delete_user method
    # delete_user - delete user from DB
    def delete_user(user_id: str) -> bool:
        # Line 83: db - create session
        db: Session = SessionLocal()
        # Line 84: user - get user
        user = UserRepository.get_by_id(db, user_id)
        # Line 85: if not user: - check existence
        if not user:
            # Line 86: db.close() - close
            db.close()
            # Line 87: return False - not found
            return False

        # Line 88: UserRepository.delete() - delete user through repository
        # db, user - pass session and user object
        UserRepository.delete(db, user)
        # Line 89: db.commit() - save changes (deletion)
        db.commit()
        # Line 90: db.close() - close session
        db.close()
        # Line 91: return True - successful
        return True


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 11:
# ==========================================================
# 
# 1. What's the difference between Repository and Service?
#    Why need service layer if repository already works with DB?
#
# 2. What does prefix _ in method name _user_to_dict mean?
#    Why make methods private?
#
# 3. What is getattr() and why use it?
#    What's the difference between user.role and getattr(user, "role", "user")?
#
# 4. What does syntax dict | None (Python 3.10+) mean?
#    How does it differ from Optional[dict]?
#
# 5. Why need to close DB session (db.close())?
#    What will happen if don't close session?
#
# 6. What is list comprehension [func(x) for x in items]?
#    What are its advantages over regular for loop?
#
# 7. Why convert User objects to dictionaries (dict)?
#    Why doesn't API return objects directly?
#
# 8. Why do ban_user, unban_user, make_admin methods change object directly (user.status = ...)?
#    Can use UserRepository.update_status() instead?
#
# 9. What's the difference between is_admin and is_superadmin?
#    Why is superadmin considered admin (is_admin = True)?
#
# 10. Why do methods return bool (True/False)?
#     How to handle error if need to return more detailed information?
#
# ==========================================================
