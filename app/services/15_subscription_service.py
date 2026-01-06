# ==========================================================
# LESSON 15: MODULE 6 - SERVICES (Business Logic)
# subscription_service.py - Service for working with subscriptions
# 
# This file contains the SubscriptionService class with business logic for subscriptions:
# getting plans, confirming payments, creating subscriptions.
# ==========================================================

# Line 1: Comment with file path

# Line 2: Import uuid for generating unique IDs
import uuid
# Line 3: Import logging for logging
import logging
# Line 4: Import classes from datetime
from datetime import datetime, timedelta, timezone
# datetime - for working with dates/time
# timedelta - for calculating time intervals (e.g., +30 days)
# timezone - for working with timezones (UTC)
from typing import List, Dict, Any
# List, Dict, Any - types for annotations (List = list, Dict = dictionary, Any = any type)

# Line 5: Import Session from SQLAlchemy
from sqlalchemy.orm import Session

# Line 6: Import SessionLocal from database.py (lesson 3)
from app.db.database import SessionLocal
# Line 7: Import SubscriptionRepository from subscription_repository.py (lesson 9)
from app.db.subscription_repository import SubscriptionRepository
# Line 8: Import UserRepository from user_repository.py (lesson 8)
from app.db.user_repository import UserRepository
# Line 9: Import Subscription model from subscription.py (lesson 5)
from app.models.subscription import Subscription
# Line 10: Import constants from constants.py (lesson 2)
from app.core.constants import (
    # SUBSCRIPTION_PLANS - dictionary with subscription plans
    SUBSCRIPTION_PLANS,
    # SUPPORTED_NETWORKS - list of supported networks
    SUPPORTED_NETWORKS,
    # NETWORK_WALLETS - dictionary with project wallets by networks
    NETWORK_WALLETS,
    # SUBSCRIPTION_STATUS_ACTIVE - constant for active status
    SUBSCRIPTION_STATUS_ACTIVE,
    # USER_ROLE_SUBSCRIBER - constant for subscriber role
    USER_ROLE_SUBSCRIBER,
    # USER_ROLE_ADMIN - constant for admin role
    USER_ROLE_ADMIN,
)
# Line 11: Import DiscordService from discord_service.py (lesson 14)
from app.services.discord_service import DiscordService
# Line 12: Import PaymentService from payment_service.py (lesson 13)
from app.services.payment_service import PaymentService
# Line 13: Import log_action function from logger.py
from app.core.logger import log_action

# Line 14: logger - create logger for this module
logger = logging.getLogger(__name__)


# Line 15: Empty line for readability


# Line 16: Definition of SubscriptionService class
class SubscriptionService:
    # Line 17: Comment - plans and networks section
    # ======================================================
    # PLANS AND NETWORKS
    # ======================================================

    # Line 18: @staticmethod decorator
    @staticmethod
    # Line 19: Definition of get_plans_and_networks method
    # get_plans_and_networks - get list of plans and networks
    # -> dict - returns dictionary with plans and networks
    def get_plans_and_networks() -> dict:
        # Line 20: Method docstring
        """
        Returns list of plans and networks with project wallets.
        """
        # Line 21: plans - create list of plans using list comprehension
        # [expression for element in collection] - list generator
        plans = [
            # Line 22: Dictionary with plan data for each plan
            {
                # Line 23: "code": code - plan code (key from SUBSCRIPTION_PLANS)
                "code": code,
                # Line 24: "title": cfg["title"] - plan title
                "title": cfg["title"],
                # Line 25: "days": cfg["days"] - number of days
                "days": cfg["days"],
                # Line 26: "price_usd": cfg["price_usd"] - price in USD
                "price_usd": cfg["price_usd"],
            }
            # Line 27: for code, cfg in SUBSCRIPTION_PLANS.items() - iterate over plans
            # .items() - get (key, value) pairs from dictionary
            for code, cfg in SUBSCRIPTION_PLANS.items()
        ]
        # Result: list of dictionaries with plans for API

        # Line 28: networks - create list of networks using list comprehension
        networks = [
            # Line 29: Dictionary with network data for each network
            {
                # Line 30: "code": net - network code
                "code": net,
                # Line 31: "wallet": NETWORK_WALLETS.get(net) - project wallet for network
                "wallet": NETWORK_WALLETS.get(net)
                # .get() - safe retrieval (returns None if key doesn't exist)
            }
            # Line 32: for net in SUPPORTED_NETWORKS - iterate over supported networks
            for net in SUPPORTED_NETWORKS
        ]

        # Line 33: return - return dictionary with plans and networks
        return {"plans": plans, "networks": networks}
        # Response structure: {"plans": [...], "networks": [...]}

    # Line 34: Comment - separator
    # ======================================================

    # Line 35: @staticmethod decorator
    @staticmethod
    # Line 36: Definition of confirm_subscription method
    # confirm_subscription - confirm subscription after payment
    # user_id: str - user ID
    # network: str - blockchain network for payment
    # plan_code: str - plan code (month, quarter, year)
    # tx_hash: str - transaction hash in blockchain
    # -> dict - returns dictionary with created subscription data
    def confirm_subscription(user_id: str, network: str, plan_code: str, tx_hash: str) -> dict:
        # Line 37: if plan_code not in SUBSCRIPTION_PLANS - validate plan
        if plan_code not in SUBSCRIPTION_PLANS:
            # Line 38: raise ValueError - raise exception
            raise ValueError(f"Invalid plan code: {plan_code}")
            # Why: cannot create subscription with non-existent plan

        # Line 39: plan - get plan data from dictionary
        plan = SUBSCRIPTION_PLANS[plan_code]
        # Line 40: days - get number of days from plan
        days = plan["days"]
        # Line 41: required_amount - get required amount from plan
        required_amount = plan["price_usd"]
        # Why: need to verify that user paid enough

        # Line 42: expected_wallet - get project wallet for network
        expected_wallet = NETWORK_WALLETS.get(network)
        # Line 43: if not expected_wallet - check that wallet is configured
        if not expected_wallet:
            # Line 44: raise ValueError - wallet not configured
            raise ValueError(f"Wallet for network '{network}' not configured")
            # Why: cannot verify payment if we don't know where it should have gone

        # Line 45: db - create DB session
        db: Session = SessionLocal()
        # Line 46: try - start of error handling block
        try:
            # Line 47: Comment - protection against reuse
            # protection against tx_hash reuse
            # Line 48: if SubscriptionRepository.tx_hash_exists(...) - check if tx_hash exists
            if SubscriptionRepository.tx_hash_exists(db, tx_hash):
                # Line 49: raise ValueError - tx_hash already used
                raise ValueError("This transaction hash has already been used")
                # Why: cannot use same transaction twice (protection against duplicates)

            # Line 50: Comment - verify transaction on blockchain
            # verify transaction on blockchain (dev / prod logic inside PaymentService)
            # Line 51: paid_amount - call PaymentService to verify transaction
            # verify_transaction() - method verifies transaction on blockchain
            paid_amount = PaymentService.verify_transaction(
                # Line 52: network=network - network name
                network=network,
                # Line 53: tx_hash=tx_hash - transaction hash
                tx_hash=tx_hash,
                # Line 54: expected_to_address=expected_wallet - expected recipient address
                expected_to_address=expected_wallet,
                # Line 55: min_amount_required=required_amount - minimum required amount
                min_amount_required=required_amount,
            )
            # Result: actual payment amount (in network's native token)

            # Line 56: if paid_amount < required_amount - check amount sufficiency
            if paid_amount < required_amount:
                # Line 57: raise ValueError - insufficient amount
                raise ValueError("Insufficient payment amount")
                # Why: cannot activate subscription if paid less than required

            # Line 58: now - current time in UTC
            now = datetime.now(timezone.utc)
            # Line 59: expires_at - subscription expiration date
            # now + timedelta(days=days) - current time + number of days from plan
            expires_at = now + timedelta(days=days)
            # Example: if now is January 1, days=30, then expires_at = January 31

            # Line 60: subscription - create Subscription object
            subscription = Subscription(
                # Line 61: user_id=user_id - user ID
                user_id=user_id,
                # Line 62: network=network - blockchain network
                network=network,
                # Line 63: tx_hash=tx_hash - transaction hash
                tx_hash=tx_hash,
                # Line 64: amount=paid_amount - actual paid amount
                amount=paid_amount,
                # Line 65: plan_code=plan_code - plan code
                plan_code=plan_code,
                # Line 66: status=SUBSCRIPTION_STATUS_ACTIVE - active subscription status
                status=SUBSCRIPTION_STATUS_ACTIVE,
                # Line 67: expires_at=expires_at - expiration date
                expires_at=expires_at,
            )
            # Line 68: subscription - save subscription to DB
            subscription = SubscriptionRepository.create(db, subscription)

            # Line 69: Comment - update user role
            # Update user role in DB
            # Line 70: user - get user by ID
            user = UserRepository.get_by_id(db, user_id)
            # Line 71: if user and user.role != USER_ROLE_ADMIN - check that user exists and is not admin
            # Admins remain admins, regular users become subscribers
            if user and user.role != USER_ROLE_ADMIN:
                # Line 72: user.role = USER_ROLE_SUBSCRIBER - set subscriber role
                user.role = USER_ROLE_SUBSCRIBER
                # Line 73: db.commit() - save changes
                db.commit()
                # Line 74: db.refresh(user) - refresh object
                db.refresh(user)

                # Line 75: Comment - grant Discord role
                # If Discord is linked — immediately try to grant role
                # Line 76: if user.discord_id - check that Discord account is linked
                if user.discord_id:
                    # Line 77: try - start of block for Discord error handling
                    try:
                        # Line 78: DiscordService.add_subscriber_role() - grant role in Discord
                        DiscordService.add_subscriber_role(user.discord_id)
                    # Line 79: except Exception - catch any errors
                    except Exception as e:
                        # Line 80: logger.error - log error
                        logger.error("Failed to add Discord role on payment: %s", e)
                        # Why: don't let Discord error break subscription creation

            # Line 81: Comment - log payment
            # Log payment
            # Line 82: log_action() - call admin action logging function
            # In this case we log user action (user_id as admin_id)
            log_action(
                # Line 83: action="subscription_paid" - action name
                action="subscription_paid",
                # Line 84: admin_id=user_id - user ID (who performed)
                admin_id=user_id,
                # Line 85: target_id=user_id - target ID (same user)
                target_id=user_id,
                # Line 86: details - action details (f-string for formatting)
                details=f"plan={plan_code}, network={network}, tx={tx_hash[:10]}...",
                # tx_hash[:10] - first 10 characters of hash (for brevity)
            )

            # Line 87: return - return subscription data
            return {
                # Line 88: "id": subscription.id - subscription ID
                "id": subscription.id,
                # Line 89: "user_id": subscription.user_id - user ID
                "user_id": subscription.user_id,
                # Line 90: "plan_code": subscription.plan_code - plan code
                "plan_code": subscription.plan_code,
                # Line 91: "status": subscription.status - status
                "status": subscription.status,
                # Line 92: "expires_at" - expiration date in ISO format
                "expires_at": subscription.expires_at.isoformat() if subscription.expires_at else None,
                # Line 93: "created_at" - creation date in ISO format
                "created_at": subscription.created_at.isoformat() if subscription.created_at else None,
            }
        # Line 94: finally - block always executes
        finally:
            # Line 95: db.close() - close DB session
            db.close()


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 15:
# ==========================================================
# 
# 1. Why do we need the get_plans_and_networks() method?
#    Why not return SUBSCRIPTION_PLANS and NETWORK_WALLETS directly?
#
# 2. What is list comprehension and what are its advantages?
#    How does [dict for code, cfg in SUBSCRIPTION_PLANS.items()] work?
#
# 3. Why check tx_hash_exists before creating subscription?
#    What problem will arise if we don't check for duplicate tx_hash usage?
#
# 4. How does PaymentService.verify_transaction() work?
#    What happens if transaction is not found on blockchain?
#
# 5. Why check paid_amount >= required_amount?
#    What will happen if user pays less than required amount?
#
# 6. Why don't admins (USER_ROLE_ADMIN) get subscriber role?
#    What logic is behind this check?
#
# 7. Why grant Discord role immediately after payment?
#    What will happen if granting Discord role fails?
#
# 8. Why log subscription_paid action?
#    What information is important in the log's details field?
#
# 9. Why use finally to close session?
#    What will happen if we don't close session on error?
#
# 10. What's the difference between expires_at and created_at?
#     How is expires_at calculated based on plan?
#
# ==========================================================

