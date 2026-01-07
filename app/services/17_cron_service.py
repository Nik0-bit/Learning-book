# ==========================================================
# LESSON 17: MODULE 6 - SERVICES (Business Logic)
# cron_service.py - Service for background tasks (cron jobs)
# 
# This file contains functions for automatic synchronization of Discord roles
# with user subscriptions. Runs in background thread periodically.
# ==========================================================

# Line 1: Comment with file path

# Line 2: Import time module for working with time
import time
# time.sleep() - function to pause execution for specified number of seconds
# Line 3: Import threading module for working with threads
import threading
# threading - module for creating multithreaded applications
# Thread - class for creating separate execution thread
# Line 4: Import logging for logging
import logging
# Line 5: Import datetime for working with dates
from datetime import datetime

# Line 6: Import Session from SQLAlchemy
from sqlalchemy.orm import Session

# Line 7: Import SessionLocal from database.py (lesson 3)
from app.db.database import SessionLocal
# Line 8: Import User model from user.py (lesson 4)
from app.models.user import User
# Line 9: Import SubscriptionRepository from subscription_repository.py (lesson 9)
from app.db.subscription_repository import SubscriptionRepository
# Line 10: Import DiscordService from discord_service.py (lesson 14)
from app.services.discord_service import DiscordService
# Line 11: Import log_action function from logger.py
from app.core.logger import log_action

# Line 12: logger - create logger for this module
logger = logging.getLogger(__name__)

# Line 13: SYNC_INTERVAL_HOURS - synchronization interval in hours
# Constant defines how often to run synchronization
SYNC_INTERVAL_HOURS = 24  # every 24 hours
# Why: periodic check and synchronization of Discord roles with subscriptions


# Line 14: Empty line for readability


# Line 15: Definition of sync_all_discord_roles function
# sync_all_discord_roles - function to synchronize all Discord roles
# Function checks all users with linked Discord and synchronizes their roles
def sync_all_discord_roles():
    # Line 16: Function docstring
    """
    Full automatic synchronization of Discord roles.
    Logic:

    - Get all users who have discord_id.
    - For each check active subscription.
    - If active subscription exists — grant role.
    - If missing — remove role.
    """
    # Synchronization = bringing Discord roles in line with subscriptions

    # Line 17: db - create DB session
    db: Session = SessionLocal()
    # Line 18: try - start of error handling block
    try:
        # Line 19: users - get all users with linked Discord
        # db.query(User) - query to users table
        # .filter(User.discord_id.isnot(None)) - filter: discord_id is not None
        # .all() - get all records
        users = db.query(User).filter(User.discord_id.isnot(None)).all()
        # isnot(None) = SQL operator IS NOT NULL (check that field is not empty)
    # Line 20: except Exception - catch any errors
    except Exception as e:
        # Line 21: logger.exception - log exception with full trace
        logger.exception("[CRON] Failed to load users")
        # exception() - logs exception with full stack trace (for debugging)
        # Line 22: db.close() - close session
        db.close()
        # Line 23: return - exit function on error
        return
        # Why: don't continue if we couldn't load users

    # Line 24: logger.info - log start of synchronization
    logger.info("[CRON] Sync started — %s users found", len(users))
    # %s - placeholder for string (len(users) will be substituted for %s)

    # Line 25: for user in users: - loop through all users
    for user in users:
        # Line 26: try - start of error handling block for each user
        try:
            # Line 27: active_sub - get user's active subscription
            # SubscriptionRepository.get_active_by_user_id() - method to get active subscription
            active_sub = SubscriptionRepository.get_active_by_user_id(db, user.id)
            # active_sub will be Subscription object or None

            # Line 28: if active_sub: - check that active subscription exists
            if active_sub:
                # Line 29: Comment - active subscription exists
                # active subscription exists → role should be granted
                # Line 30: try - start of block for granting role
                try:
                    # Line 31: DiscordService.add_subscriber_role() - grant subscriber role
                    DiscordService.add_subscriber_role(user.discord_id)
                    # Why: synchronize role - if subscription exists, role should exist
                # Line 32: except Exception - catch Discord errors
                except Exception as e:
                    # Line 33: logger.error - log error
                    logger.error("[CRON] Failed to add role for user %s: %s", user.id, e)
                    # Why: log error, but continue for other users

                # Line 34: log_action() - log action
                log_action(
                    # Line 35: action="cron_role_sync_add" - action name
                    action="cron_role_sync_add",
                    # Line 36: admin_id=user.id - user ID (who performed)
                    admin_id=user.id,
                    # Line 37: target_id=user.id - target ID (same user)
                    target_id=user.id,
                    # Line 38: details - action details
                    details=f"active subscription: {active_sub.plan_code}",
                )

            # Line 39: else: - block for case when no active subscription
            else:
                # Line 40: Comment - no active subscription
                # no active subscription → remove role
                # Line 41: try - start of block for removing role
                try:
                    # Line 42: DiscordService.remove_subscriber_role() - remove role
                    DiscordService.remove_subscriber_role(user.discord_id)
                    # Why: if subscription expired - remove role
                # Line 43: except Exception - catch Discord errors
                except Exception as e:
                    # Line 44: logger.error - log error
                    logger.error("[CRON] Failed to remove role for user %s: %s", user.id, e)

                # Line 45: log_action() - log action
                log_action(
                    # Line 46: action="cron_role_sync_remove" - action name
                    action="cron_role_sync_remove",
                    # Line 47: admin_id=user.id - user ID
                    admin_id=user.id,
                    # Line 48: target_id=user.id - target ID
                    target_id=user.id,
                    # Line 49: details - action details
                    details="subscription expired or missing",
                )

        # Line 50: except Exception - catch errors when processing one user
        except Exception as e:
            # Line 51: logger.error - log error
            logger.error("[CRON] Unexpected error syncing user %s: %s", user.id, e)
            # Why: log error, but continue for other users

    # Line 52: logger.info - log completion of synchronization
    logger.info("[CRON] Sync finished")

    # Line 53: db.close() - close DB session
    db.close()
    # Why: free connection resources


# Line 54: Empty line for readability


# Line 55: Definition of start_cron_background_thread function
# start_cron_background_thread - start background thread for periodic synchronization
def start_cron_background_thread():
    # Line 56: Function docstring
    """
    Starts infinite loop in separate thread,
    which calls sync_all_discord_roles every 24 hours.
    """
    # Thread = separate execution sequence (parallel to main thread)
    # Background thread = works in background, not blocking main application

    # Line 57: Definition of nested function loop
    # loop - function with infinite synchronization loop
    def loop():
        # Line 58: while True: - infinite loop
        while True:
            # Line 59: try - start of error handling block
            try:
                # Line 60: sync_all_discord_roles() - call synchronization function
                sync_all_discord_roles()
                # Synchronization of all roles is performed
            # Line 61: except Exception - catch synchronization errors
            except Exception as e:
                # Line 62: logger.exception - log exception
                logger.exception("[CRON] sync failed")
                # Why: log error, but continue loop (don't crash)

            # Line 63: time.sleep() - pause execution
            # SYNC_INTERVAL_HOURS * 3600 - convert hours to seconds
            # 24 * 3600 = 86400 seconds (24 hours)
            # sleep() - suspends thread execution for specified time
            time.sleep(SYNC_INTERVAL_HOURS * 3600)
            # After pause loop repeats (calls sync_all_discord_roles again)

    # Line 64: thread - create thread object
    # threading.Thread() - Thread class constructor to create thread
    # target=loop - function that will execute in thread
    # daemon=True - daemon thread (will terminate when main process ends)
    thread = threading.Thread(target=loop, daemon=True)
    # Comparison: thread = like separate worker that works parallel to main
    
    # Line 65: thread.start() - start thread
    thread.start()
    # Why: thread starts executing loop() function in background
    
    # Line 66: logger.info - log thread start
    logger.info("[CRON] Background sync thread started.")
    # Thread now works in background and will synchronize roles every 24 hours


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 17:
# ==========================================================
# 
# 1. What is cron job and why do we need automatic synchronization?
#    Why not synchronize roles immediately when subscription changes?
#
# 2. What is thread in programming?
#    What's the difference between main thread and background thread?
#
# 3. What does daemon=True mean when creating thread?
#    What will happen to thread when main process ends?
#
# 4. Why do we need infinite loop while True in loop() function?
#    Can we use another method for periodic execution?
#
# 5. What does time.sleep() do and why do we need pause between synchronizations?
#    What will happen if we remove sleep() from loop?
#
# 6. Why handle exceptions in loop (try/except)?
#    What will happen if we don't handle errors in infinite loop?
#
# 7. Why use db.query(User) directly, not through repository?
#    What's the difference between direct query and using repository?
#
# 8. What does isnot(None) mean in SQLAlchemy filter?
#    How is this converted to SQL query?
#
# 9. Why log each synchronization action (log_action)?
#    What information is important in synchronization logs?
#
# 10. Why don't Discord errors stop synchronization?
#     What logic is behind handling errors for each user separately?
#
# ==========================================================

