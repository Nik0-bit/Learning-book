# ==========================================================
# LESSON 8: MODULE 5 - DB/REPOSITORIES
# user_repository.py - Repository for working with users in DB
# 
# This file contains UserRepository class with methods for working with users table.
# Repository - Data Access Layer that hides DB work details.
# ==========================================================

# Line 1: Empty line (original file starts with empty line)

# Line 2: Import Session class from SQLAlchemy ORM
# From where: external SQLAlchemy library (pip install sqlalchemy)
# Session - class for database session (object for executing DB operations)
# Session = temporary DB connection for executing queries (like transaction)
from sqlalchemy.orm import Session
# Analogy: Session = like workspace - you open session, work with DB, close it

# Line 3: Import User model from models/user.py (lesson 4)
from app.models.user import User
# Why: repository works with User model (users table in DB)


# Line 4: Empty line for readability


# Line 5: Definition of UserRepository class
# class UserRepository: - creates user repository class
# Repository = design pattern (code template) for working with data
# Repository encapsulates DB logic (hides SQL queries behind methods)
class UserRepository:
    # Analogy: Repository = like library - you ask "give book by author", 
    # librarian knows where to look (hides storage details)


    # Line 6: Empty line for readability
    
    # Line 7: @staticmethod decorator
    # @staticmethod - decorator making method static
    # Static method = method that doesn't require creating class instance (can call via class)
    # Doesn't use self (no access to class instance)
    @staticmethod
    # Line 8: Definition of get_by_email method
    # get_by_email - get user by email
    # db: Session - DB session parameter (must pass)
    # email: str - user email parameter (string)
    # Function returns User object or None (if user not found)
    def get_by_email(db: Session, email: str):
        # Line 9: return - return DB query result
        # db.query(User) - start query to users table (via User model)
        # query() - Session method for creating query
        # .filter(User.email == email) - filter: where email equals passed email
        # User.email == email - comparing model email field with passed value
        # .first() - get first record (or None if nothing found)
        return db.query(User).filter(User.email == email).first()
        # What happens: SQLAlchemy generates SQL query: SELECT * FROM users WHERE email = ?
        # Analogy: like phone book search - search by name (email), find record


    # Line 10: Empty line for readability

    # Line 11: @staticmethod decorator
    @staticmethod
    # Line 12: Definition of get_by_username method
    # get_by_username - get user by username
    def get_by_username(db: Session, username: str):
        # Line 13: Similarly to get_by_email, but filter by username field
        return db.query(User).filter(User.username == username).first()
        # SQL query: SELECT * FROM users WHERE username = ?


    # Line 14: Empty line for readability

    # Line 15: @staticmethod decorator
    @staticmethod
    # Line 16: Definition of get_by_id method
    # get_by_id - get user by ID (unique identifier)
    def get_by_id(db: Session, user_id: str):
        # Line 17: Query DB by id field
        return db.query(User).filter(User.id == user_id).first()
        # SQL query: SELECT * FROM users WHERE id = ?
        # Why first(): id is unique, so always maximum one record


    # Line 18: Empty line for readability

    # Line 19: @staticmethod decorator
    @staticmethod
    # Line 20: Definition of create method
    # create - create new user in DB
    # user: User - User model object (already created in Python code, but not saved to DB)
    def create(db: Session, user: User):
        # Line 21: db.add(user) - add object to DB session
        # add() - Session method for adding object to save queue
        # Object not yet saved to DB, only added to session
        db.add(user)
        # Analogy: like putting item in cart - haven't bought yet, but prepared for purchase
        
        # Line 22: db.commit() - save changes to DB
        # commit() - method for executing all operations and saving to DB
        # Until this point changes only in memory, after commit - in database
        db.commit()
        # Analogy: like paying for purchase - before this item in cart, after commit - bought
        
        # Line 23: db.refresh(user) - refresh object from DB
        # refresh() - reload object from DB (get current data)
        # Why: after commit object can get values from DB (e.g., created_at from server_default)
        db.refresh(user)
        # Analogy: like refreshing page - get fresh data
        
        # Line 24: return user - return created user
        return user
        # Return object with current data from DB


    # Line 25: Empty line for readability

    # Line 26: @staticmethod decorator
    @staticmethod
    # Line 27: Definition of get_all method
    # get_all - get all users from DB
    # Returns list of User objects
    def get_all(db: Session):
        # Line 28: db.query(User).all() - query all records
        # query(User) - query to users table
        # .all() - get all records (unlike .first() which returns one)
        return db.query(User).all()
        # SQL query: SELECT * FROM users
        # Warning: for large tables this can be slow (better use pagination)


    # Line 29: Empty line for readability

    # Line 30: @staticmethod decorator
    @staticmethod
    # Line 31: Definition of update_status method
    # update_status - update user status
    # user: User - user object (already loaded from DB)
    # status: str - new status (e.g., "active" or "banned")
    def update_status(db: Session, user: User, status: str):
        # Line 32: user.status = status - change object attribute
        # Change status field of User object (in Python memory)
        user.status = status
        # Important: change only in memory, not yet saved to DB
        
        # Line 33: db.commit() - save changes to DB
        db.commit()
        # SQLAlchemy tracks object changes and saves them on commit
        
        # Line 34: db.refresh(user) - refresh object from DB
        db.refresh(user)
        # Line 35: return user - return updated user
        return user


    # Line 36: Empty line for readability

    # Line 37: @staticmethod decorator
    @staticmethod
    # Line 38: Definition of update_role method
    # update_role - update user role
    # Similarly to update_status, but changes role field
    def update_role(db: Session, user: User, role: str):
        # Line 39: Change user role
        user.role = role
        # Line 40: Save changes
        db.commit()
        # Line 41: Refresh object
        db.refresh(user)
        # Line 42: Return updated user
        return user


    # Line 43: Empty line for readability

    # Line 44: @staticmethod decorator
    @staticmethod
    # Line 45: Definition of delete method
    # delete - delete user from DB
    # user: User - user object to delete
    def delete(db: Session, user: User):
        # Line 46: db.delete(user) - delete object from DB session
        # delete() - Session method for deleting object
        # Object marked for deletion (not yet deleted from DB)
        db.delete(user)
        # Analogy: like marking file for deletion - not deleted yet, but will be deleted on commit
        
        # Line 47: db.commit() - execute deletion in DB
        db.commit()
        # After commit record deleted from database
        # Warning: after commit user object still exists in Python, but not in DB


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 8:
# ==========================================================
# 
# 1. What is Repository and why is it needed?
#    What advantages does using repositories give?
#
# 2. What does @staticmethod mean and why is it used?
#    Why are all methods in UserRepository static?
#
# 3. What is db.query(User) and how does it work?
#    How does SQLAlchemy convert this to SQL query?
#
# 4. What's the difference between .first() and .all() in queries?
#    When to use each?
#
# 5. What does db.add(user) do and when to call it?
#    What's the difference between add() and commit()?
#
# 6. Why is db.refresh(user) needed after commit()?
#    What data can appear after commit that wasn't before?
#
# 7. Why for updating status/role need to first change user.status, then commit?
#    Can this be done with one SQL query?
#
# 8. What happens to user object after db.delete(user) and commit()?
#    Can you use user object after it's deleted from DB?
#
# 9. Why can get_all() method be problematic for large tables?
#    How can getting all records be optimized?
#
# 10. What's the difference between filtering by email, username, and id?
#     Why is index not needed for id search (it's already there as primary_key)?
#
# ==========================================================
