# ==========================================================
# LESSON 5: MODULE 3 - MODELS
# subscription.py - Subscription Model
# 
# This file defines the structure of "subscriptions" table in the database.
# Subscription model describes user subscription: payment, plan, expiration date.
# ==========================================================

# Line 1: Empty line (original file starts with empty line)

# Line 2: Import uuid module for generating unique IDs
import uuid
# Line 3: Import column types from SQLAlchemy
# Float - data type "floating point number" (for money: 15.5, 99.99)
from sqlalchemy import Column, String, DateTime, Float
# Line 4: Import func function for SQL functions
from sqlalchemy.sql import func
# Line 5: Import Base from database.py (lesson 3)
from app.db.database import Base


# Line 6: Empty line for readability

# Line 7: Definition of Subscription class
class Subscription(Base):
    # Line 8: __tablename__ - table name in DB
    __tablename__ = "subscriptions"
    
    # Line 9: id - unique subscription identifier
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    # Line 10: user_id - ID of user who owns the subscription
    # index=True - index for fast search of user's subscriptions
    # nullable=False - required (subscription must belong to a user)
    user_id = Column(String, index=True, nullable=False)
    
    # Line 11: network - blockchain network through which payment was made
    # Comment: possible values - ethereum, polygon, arbitrum, optimism, solana
    network = Column(String, nullable=False)       # ethereum / polygon / arbitrum / optimism / solana
    # Line 12: tx_hash - transaction hash (unique payment identifier in blockchain)
    # unique=True - each tx_hash can be used only once (protection against reuse)
    # nullable=False - required (needed for payment verification)
    tx_hash = Column(String, unique=True, nullable=False)
    # Line 13: amount - paid amount in USD equivalent
    # Float - floating point number (for money: 15.0, 99.99)
    # Comment: amount stored in USD for convenience (regardless of cryptocurrency)
    amount = Column(Float, nullable=False)         # paid amount (in USD equivalent for accounting)
    # Line 14: plan_code - subscription plan code
    # Comment: possible values - month, quarter, year (from constants.py)
    plan_code = Column(String, nullable=False)     # month / quarter / year
    # Line 15: status - subscription status (active, pending, failed)
    # default="active" - active by default
    status = Column(String, nullable=False, default="active")
    
    # Line 16: expires_at - date and time of subscription expiration
    # DateTime(timezone=True) - with timezone awareness
    # nullable=False - required (need to know when it expires)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    # Line 17: created_at - date and time of subscription record creation
    # server_default=func.now() - automatically set by DB when creating
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 5:
# ==========================================================
# 
# 1. Why is unique=True needed for tx_hash?
#    What will happen if same tx_hash is used twice?
#
# 2. Why is amount stored as Float, not int (whole dollars)?
#    What problems can arise when working with money as Float?
#
# 3. What is tx_hash (transaction hash) in blockchain?
#    Why is it unique and why can't it be forged?
#
# 4. Why is index needed on user_id?
#    How often will we search subscriptions by user_id?
#
# 5. What does expires_at mean and why is it needed?
#    How does system know subscription has expired?
#
# 6. Why is network stored as String, not as separate table?
#    What are pros and cons of this approach?
#
# 7. What is plan_code and where do values month/quarter/year come from?
#    Where are plans defined (plan, price, days)?
#
# 8. Why is subscription status needed (active, pending, failed)?
#    In what sequence do they change during payment?
#
# ==========================================================
