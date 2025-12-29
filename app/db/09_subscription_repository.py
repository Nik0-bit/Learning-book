# ==========================================================
# LESSON 9: MODULE 5 - DB/REPOSITORIES
# subscription_repository.py - Repository for working with subscriptions in DB
# 
# This file contains SubscriptionRepository class with methods for working with subscriptions table.
# Repository provides methods for creating, searching, and working with user subscriptions.
# ==========================================================

# Line 1: Import datetime and timezone classes from datetime module
# From where: built-in Python module
# datetime - class for working with date and time
# timezone - class for working with timezones (UTC)
from datetime import datetime, timezone
# timezone.utc - UTC timezone object (needed for correct date handling)

# Line 2: Import List and Optional types from typing module
# From where: built-in Python module
# List[Subscription] - type "list of Subscription objects"
# Optional[Subscription] - type "Subscription or None" (can be empty)
from typing import List, Optional
# Why: type annotations help understand what function returns

# Line 3: Import Session from SQLAlchemy ORM
from sqlalchemy.orm import Session

# Line 4: Import Subscription model from models/subscription.py (lesson 5)
from app.models.subscription import Subscription
# Line 5: Import constant from constants.py (lesson 2)
from app.core.constants import SUBSCRIPTION_STATUS_ACTIVE
# SUBSCRIPTION_STATUS_ACTIVE = "active" (constant for active subscription)


# Line 6: Empty line for readability


# Line 7: Definition of SubscriptionRepository class
class SubscriptionRepository:
    # Line 8: @staticmethod decorator
    @staticmethod
    # Line 9: Definition of create method
    # create - create new subscription in DB
    # subscription: Subscription - subscription object (already created, but not saved)
    # -> Subscription - function returns Subscription object
    def create(db: Session, subscription: Subscription) -> Subscription:
        # Line 10: Function docstring (documentation)
        """
        Creates subscription in DB.
        """
        # Line 11: db.add(subscription) - add subscription to session
        db.add(subscription)
        # Line 12: db.commit() - save to DB
        db.commit()
        # Line 13: db.refresh(subscription) - refresh object from DB
        db.refresh(subscription)
        # Line 14: return subscription - return created subscription
        return subscription


    # Line 15: Empty line for readability

    # Line 16: @staticmethod decorator
    @staticmethod
    # Line 17: Definition of get_active_by_user_id method
    # get_active_by_user_id - get active subscription of user
    # -> Optional[Subscription] - returns Subscription or None (if no active subscription)
    def get_active_by_user_id(db: Session, user_id: str) -> Optional[Subscription]:
        # Line 18: Function docstring
        """
        Returns current active subscription of user (if exists).
        """
        # Line 19: now - current time in UTC
        # datetime.now(timezone.utc) - get current date/time in UTC timezone
        # timezone.utc - UTC timezone object
        now = datetime.now(timezone.utc)
        # Why: need to compare expires_at with current time to check if subscription expired
        
        # Line 20: return - return query result (multi-line query)
        return (
            # Line 21: db.query(Subscription) - query to subscriptions table
            db.query(Subscription)
            # Line 22: .filter() - applying filters to query
            # Can pass multiple conditions separated by comma (they're combined via AND)
            .filter(
                # Line 23: Subscription.user_id == user_id - filter by user ID
                Subscription.user_id == user_id,
                # Line 24: Subscription.expires_at > now - filter: expiration date greater than current
                # expires_at > now means subscription hasn't expired yet (current)
                Subscription.expires_at > now,
                # Line 25: Subscription.status == SUBSCRIPTION_STATUS_ACTIVE - filter by status
                # status == "active" means subscription is active (not pending, not failed)
                Subscription.status == SUBSCRIPTION_STATUS_ACTIVE,
            )
            # Line 26: .order_by() - sort results
            # Subscription.expires_at.desc() - sort by expires_at descending (newest to oldest)
            # desc() = descending = from larger to smaller
            .order_by(Subscription.expires_at.desc())
            # Line 27: .first() - get first record (newest active subscription)
            .first()
        )
        # SQL query approximately: SELECT * FROM subscriptions 
        # WHERE user_id = ? AND expires_at > ? AND status = 'active' 
        # ORDER BY expires_at DESC LIMIT 1
        # Analogy: like finding user's newest active subscription


    # Line 28: Empty line for readability

    # Line 29: @staticmethod decorator
    @staticmethod
    # Line 30: Definition of get_latest_by_user_id method
    # get_latest_by_user_id - get latest subscription of user (even if expired)
    # -> Optional[Subscription] - returns Subscription or None
    def get_latest_by_user_id(db: Session, user_id: str) -> Optional[Subscription]:
        # Line 31: Function docstring
        """
        Latest subscription of user (even if already expired).
        """
        # Line 32: return - return query result
        return (
            # Line 33: db.query(Subscription) - query to table
            db.query(Subscription)
            # Line 34: .filter(Subscription.user_id == user_id) - filter only by user_id
            # No filters by expires_at and status - get any subscription of user
            .filter(Subscription.user_id == user_id)
            # Line 35: .order_by(Subscription.created_at.desc()) - sort by creation date
            # created_at.desc() - newest to oldest (most recently created)
            .order_by(Subscription.created_at.desc())
            # Line 36: .first() - get first record (latest one)
            .first()
        )
        # SQL query: SELECT * FROM subscriptions WHERE user_id = ? ORDER BY created_at DESC LIMIT 1
        # Why: get latest subscription regardless of status (for history, analytics)


    # Line 37: Empty line for readability

    # Line 38: @staticmethod decorator
    @staticmethod
    # Line 39: Definition of get_history_by_user_id method
    # get_history_by_user_id - get full subscription history of user
    # -> List[Subscription] - returns list of Subscription objects
    def get_history_by_user_id(db: Session, user_id: str) -> List[Subscription]:
        # Line 40: Function docstring
        """
        Full subscription history of user (newest to oldest).
        """
        # Line 41: return - return query result
        return (
            # Line 42: db.query(Subscription) - query to table
            db.query(Subscription)
            # Line 43: .filter(Subscription.user_id == user_id) - filter by user_id
            .filter(Subscription.user_id == user_id)
            # Line 44: .order_by(Subscription.created_at.desc()) - sort by creation date
            .order_by(Subscription.created_at.desc())
            # Line 45: .all() - get all records (unlike .first())
            .all()
        )
        # SQL query: SELECT * FROM subscriptions WHERE user_id = ? ORDER BY created_at DESC
        # Why: get all user subscriptions for history (all active, expired, failed)


    # Line 46: Empty line for readability

    # Line 47: @staticmethod decorator
    @staticmethod
    # Line 48: Definition of tx_hash_exists method
    # tx_hash_exists - check if transaction exists (by hash)
    # tx_hash = transaction hash = transaction hash in blockchain
    # -> bool - returns True (exists) or False (doesn't exist)
    def tx_hash_exists(db: Session, tx_hash: str) -> bool:
        # Line 49: Function docstring
        """
        Check for already used transaction hash.
        """
        # Line 50: return - return check result
        return (
            # Line 51: db.query(Subscription.id) - query only id field (not full object)
            # query(Subscription.id) - query only id for optimization (don't need all data)
            db.query(Subscription.id)
            # Line 52: .filter(Subscription.tx_hash == tx_hash) - filter by tx_hash
            .filter(Subscription.tx_hash == tx_hash)
            # Line 53: .first() - get first record (or None)
            .first()
            # Line 54: is not None - check that result is not None
            # If .first() returned record (not None) - means tx_hash exists (True)
            # If .first() returned None - means tx_hash not found (False)
            is not None
        )
        # SQL query: SELECT id FROM subscriptions WHERE tx_hash = ? LIMIT 1
        # Why: check if this tx_hash was already used (protection against payment reuse)
        # Analogy: like passport check - if already in database, means already used


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 9:
# ==========================================================
# 
# 1. What's the difference between get_active_by_user_id and get_latest_by_user_id?
#    When to use each method?
#
# 2. Why is filter Subscription.expires_at > now needed in get_active_by_user_id?
#    What will happen if remove this filter?
#
# 3. What does .order_by(Subscription.expires_at.desc()) mean?
#    Why sort results before .first()?
#
# 4. Why in get_active_by_user_id filter by expires_at, status and user_id?
#    Can inactive subscription be retrieved if remove status filter?
#
# 5. Why is get_history_by_user_id method needed if there's get_latest_by_user_id?
#    In what cases is full subscription history needed?
#
# 6. What is tx_hash and why check if it exists?
#    What problem will arise if don't check tx_hash_exists before creating subscription?
#
# 7. Why in tx_hash_exists query only Subscription.id, not full object?
#    What advantage does querying only id give?
#
# 8. What does is not None mean and how does it work?
#    Why can .first() return None?
#
# 9. What's the difference between .first() and .all()?
#    When to use each?
#
# 10. Why is timezone.utc needed when working with dates?
#     What problems can arise if don't specify timezone?
#
# ==========================================================
