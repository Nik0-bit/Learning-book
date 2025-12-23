# ==========================================================
# LESSON 3: MODULE 2 - DB (Database)
# database.py - Database Connection
# 
# This file sets up connection to SQLite database
# and creates necessary objects for working with ORM (SQLAlchemy).
# ==========================================================

# Line 1: Import create_engine function from SQLAlchemy library
# From where: external library (pip install sqlalchemy)
# What is this: SQLAlchemy - ORM (Object-Relational Mapping) for working with databases
# ORM = way to work with DB through Python objects instead of SQL queries
# create_engine - function to create "engine" (DB connection)
from sqlalchemy import create_engine
# Analogy: create_engine = like car key - you create key to start the car (DB)
# What is ORM: instead of "SELECT * FROM users WHERE id = 1" you write db.query(User).filter(User.id == 1)

# Line 2: Import functions from SQLAlchemy ORM module
# sessionmaker - function to create DB session factory
# declarative_base - function to create base class for models
# Session = DB session = temporary connection for executing operations (like transaction)
# Base = base class from which all models (tables) inherit in DB
from sqlalchemy.orm import sessionmaker, declarative_base
# sessionmaker = like factory for creating sessions (like printing press for sessions)
# declarative_base = like template for all models (all models inherit from Base)


# Line 3: Empty line for readability (separates imports and code)


# Line 4: SQLALCHEMY_DATABASE_URL - database connection string
# This is URL (address) of database in special SQLAlchemy format
# "sqlite:///./akiro.db" - format for SQLite database
# sqlite:/// - connection protocol (SQLite through file)
# ./akiro.db - path to database file (./ = current directory, akiro.db = filename)
# SQLite = file-based database (entire DB in one file, no separate server needed)
SQLALCHEMY_DATABASE_URL = "sqlite:///./akiro.db"
# Analogy: like house address - sqlite:/// = protocol (like "http://"), ./akiro.db = file path
# What is SQLite: lightweight database, stored in file (like Excel file, but for structured data)


# Line 5: Empty line for readability


# Line 6: engine - database engine creation
# create_engine() - function call to create engine
# Engine = object that manages DB connection and executes queries
engine = create_engine(
    # Line 7: SQLALCHEMY_DATABASE_URL - pass connection string
    # This is required parameter - where to connect
    SQLALCHEMY_DATABASE_URL,
    # Line 8: connect_args - additional connection arguments
    # {"check_same_thread": False} - dictionary with SQLite settings
    # check_same_thread=False - allow DB usage from different threads
    # Why: FastAPI works asynchronously (multiple threads), need to allow access from any thread
    # If True - DB will be available only from thread where engine was created (error in FastAPI)
    connect_args={"check_same_thread": False}
)
# Analogy: engine = like car engine - it manages all the work (DB)
# check_same_thread=False = like multi-user access - several people can work simultaneously


# Line 9: Empty line for readability


# Line 10: SessionLocal - factory for creating database sessions
# sessionmaker() - function call to create factory
# Factory = function that creates objects (sessions) when called
# SessionLocal() - calling this factory will create new DB session
SessionLocal = sessionmaker(
    # Line 11: autocommit=False - automatic commit disabled
    # autocommit = automatic saving of changes to DB
    # False = need to manually call db.commit() to save
    # Why: more control - can rollback changes if something went wrong
    autocommit=False,
    # Line 12: autoflush=False - automatic synchronization disabled
    # autoflush = automatic sending of changes to DB before queries
    # False = need to manually call db.flush() if need to synchronize
    autoflush=False,
    # Line 13: expire_on_commit=False - objects remain accessible after commit
    # expire = expire (objects become invalid)
    # False = after db.commit() objects remain accessible with current data
    # If True - after commit need to query objects from DB again
    expire_on_commit=False,
    # Line 14: bind=engine - binding factory to engine
    # bind = binding, connection
    # engine - our DB engine created above
    # Why: factory needs to know which DB to create sessions for
    bind=engine,
)
# Analogy: SessionLocal = like stamp for documents - every time you need document (session),
# you stamp new one (SessionLocal() creates new session)
# autocommit=False = like draft - you write, check, then only save (commit)


# Line 15: Empty line for readability


# Line 16: Base - base class for all models (tables) in DB
# declarative_base() - function call creates base class
# Base = class from which all models will inherit (User, Subscription, etc.)
# Model = Python class that represents table in DB
Base = declarative_base()
# Analogy: Base = like common template for all DB tables - all models get basic functionality from it
# Why: all models inherit from Base and automatically become tables in DB
# Example: class User(Base): - User becomes "users" table in DB


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 3:
# ==========================================================
# 
# 1. What is ORM and why is it needed?
#    Why use ORM instead of direct SQL queries?
#
# 2. What is SQLite and how does it differ from PostgreSQL or MySQL?
#    When to use SQLite, and when to use full DB server?
#
# 3. What does connection string "sqlite:///./akiro.db" mean?
#    What will happen if akiro.db file doesn't exist?
#
# 4. What is engine in SQLAlchemy?
#    Why need separate object for managing connection?
#
# 5. Why is parameter check_same_thread=False needed for SQLite?
#    What will happen if set True in FastAPI application?
#
# 6. What is sessionmaker and why need session factory?
#    Why not create sessions directly via Session()?
#
# 7. What does autocommit=False mean?
#    What's the advantage of manual commit over automatic?
#
# 8. What is expire_on_commit and why disable it (False)?
#    What problem can arise if set True?
#
# 9. What is Base = declarative_base()?
#    Why do all models inherit from Base?
#
# 10. How does DB work: creating engine → sessionmaker → session?
#     What happens when you call SessionLocal()?
#
# ==========================================================
