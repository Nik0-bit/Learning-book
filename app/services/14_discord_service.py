# ==========================================================
# LESSON 14: MODULE 6 - SERVICES (Business Logic)
# discord_service.py - Service for Discord integration
# 
# This file contains the DiscordService class for working with Discord API:
# OAuth2 authorization, account linking, working with server roles.
# ==========================================================

# Line 1: Import urlencode function from urllib.parse module
# From where: built-in Python module
# urlencode - function to convert dictionary to URL query string (request parameters)
from urllib.parse import urlencode
# Example: {"a": 1, "b": 2} → "a=1&b=2"
# Why: form URL with parameters for Discord OAuth2

# Line 2: Empty line for readability

# Line 3: Import httpx for HTTP requests
import httpx
# Line 4: Import logging for logging
import logging
# Line 5: Import Session from SQLAlchemy
from sqlalchemy.orm import Session
# Line 6: Import IntegrityError from SQLAlchemy
# IntegrityError - exception for database integrity errors (duplicates, constraint violations)
from sqlalchemy.exc import IntegrityError
# Why: handle errors when trying to link already used Discord ID

# Line 7: Import SessionLocal from database.py (lesson 3)
from app.db.database import SessionLocal
# Line 8: Import UserRepository from user_repository.py (lesson 8)
from app.db.user_repository import UserRepository
# Line 9: Import constants from config.py (lesson 1)
from app.core.config import (
    # DISCORD_CLIENT_ID - Discord application ID (for OAuth)
    DISCORD_CLIENT_ID,
    # DISCORD_CLIENT_SECRET - application secret key
    DISCORD_CLIENT_SECRET,
    # DISCORD_REDIRECT_URI - URI for redirect after authorization
    DISCORD_REDIRECT_URI,
    # DISCORD_BOT_TOKEN - bot token for working with server
    DISCORD_BOT_TOKEN,
    # DISCORD_GUILD_ID - Discord server (guild) ID
    DISCORD_GUILD_ID,
    # DISCORD_SUBSCRIBER_ROLE_ID - subscriber role ID on server
    DISCORD_SUBSCRIBER_ROLE_ID,
    # DISCORD_REQUIRE_GUILD_MEMBERSHIP - whether to require server membership
    DISCORD_REQUIRE_GUILD_MEMBERSHIP,
)

# Line 10: DISCORD_API - base URL for Discord API
# Constant with URL for all requests to Discord API
DISCORD_API = "https://discord.com/api"
# Line 11: logger - create logger for this module
logger = logging.getLogger(__name__)


# Line 12: Empty line for readability


# Line 13: Definition of DiscordService class
class DiscordService:
    # Line 14: Comment - OAuth2 section
    # ---------- OAuth2 ----------
    # OAuth2 - authorization protocol (user grants access to their Discord account)

    # Line 15: @staticmethod decorator
    @staticmethod
    # Line 16: Definition of get_authorize_url method
    # get_authorize_url - form URL for Discord authorization
    # state: str - state (token for CSRF attack protection)
    # -> str - returns URL string
    def get_authorize_url(state: str) -> str:
        # Line 17: Method docstring
        """
        Forms Discord OAuth2 authorization URL.
        We use scope 'identify' because we only need user profile.
        """
        # scope = access scope (what data we request from Discord)
        
        # Line 18: params - dictionary with OAuth2 request parameters
        params = {
            # Line 19: "client_id" - Discord application ID
            "client_id": DISCORD_CLIENT_ID,
            # Line 20: "redirect_uri" - where to redirect after authorization
            "redirect_uri": DISCORD_REDIRECT_URI,
            # Line 21: "response_type": "code" - response type (authorization code)
            "response_type": "code",
            # Line 22: "scope": "identify" - requested permissions (profile only)
            "scope": "identify",
            # Line 23: "state" - state for CSRF protection
            "state": state,
            # Line 24: "prompt": "consent" - always show consent screen
            "prompt": "consent",
        }
        # Line 25: return - form and return full URL
        # f"{DISCORD_API}/oauth2/authorize" - base URL of authorization endpoint
        # urlencode(params) - convert dictionary to query string
        # ? - start of parameters in URL
        return f"{DISCORD_API}/oauth2/authorize?{urlencode(params)}"
        # Example result: https://discord.com/api/oauth2/authorize?client_id=123&redirect_uri=...

    # Line 26: @staticmethod decorator
    @staticmethod
    # Line 27: Definition of exchange_code_for_token method
    # exchange_code_for_token - exchange authorization code for access token
    # code: str - authorization code (received after redirect from Discord)
    # -> dict - returns dictionary with access token
    def exchange_code_for_token(code: str) -> dict:
        # Line 28: Method docstring
        """
        Exchange authorization code for access_token.
        """
        # Line 29: data - data for token request
        data = {
            # Line 30: "client_id" - application ID
            "client_id": DISCORD_CLIENT_ID,
            # Line 31: "client_secret" - secret key (to verify request is from us)
            "client_secret": DISCORD_CLIENT_SECRET,
            # Line 32: "grant_type": "authorization_code" - request type (code exchange for token)
            "grant_type": "authorization_code",
            # Line 33: "code" - authorization code (received from Discord)
            "code": code,
            # Line 34: "redirect_uri" - must match the one from authorization request
            "redirect_uri": DISCORD_REDIRECT_URI,
        }

        # Line 35: headers - HTTP request headers
        # "Content-Type": "application/x-www-form-urlencoded" - data format (form, not JSON)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # Line 36: with httpx.Client() - create HTTP client
        with httpx.Client(timeout=10.0) as client:
            # Line 37: r - send POST request to exchange code for token
            # client.post() - POST request
            # f"{DISCORD_API}/oauth2/token" - endpoint to get token
            # data=data - send data in form format (not JSON!)
            # headers=headers - request headers
            r = client.post(f"{DISCORD_API}/oauth2/token", data=data, headers=headers)

        # Line 38: if r.status_code != 200 - check response status
        if r.status_code != 200:
            # Line 39: raise ValueError - raise exception on error
            raise ValueError(f"Token exchange error: {r.text}")
            # r.text - response text with error

        # Line 40: return r.json() - return JSON response (contains access_token)
        return r.json()
        # Response contains: access_token, token_type, expires_in etc.

    # Line 41: @staticmethod decorator
    @staticmethod
    # Line 42: Definition of fetch_discord_user method
    # fetch_discord_user - get Discord user profile
    # access_token: str - access token (obtained from exchange_code_for_token)
    # -> dict - returns dictionary with profile data
    def fetch_discord_user(access_token: str) -> dict:
        # Line 43: Method docstring
        """
        Get user profile from Discord by user access_token.
        """
        # Line 44: headers - headers with authorization token
        # "Authorization": f"Bearer {access_token}" - Bearer token in header
        # Bearer = authorization type (standard format for OAuth2)
        headers = {"Authorization": f"Bearer {access_token}"}

        # Line 45: with httpx.Client() - create HTTP client
        with httpx.Client(timeout=10.0) as client:
            # Line 46: r - GET request to get profile
            # "/users/@me" - special endpoint to get own profile
            # @me = myself (profile of user whose token is used)
            r = client.get(f"{DISCORD_API}/users/@me", headers=headers)

        # Line 47: if r.status_code != 200 - check status
        if r.status_code != 200:
            # Line 48: raise ValueError - raise exception
            raise ValueError(f"Discord user fetch failed: {r.text}")

        # Line 49: return r.json() - return profile data
        return r.json()
        # Response contains: id, username, discriminator, avatar etc.


    # Line 50: Comment - account linking/unlinking section
    # ---------- Link / Unlink ----------

    # Line 51: @staticmethod decorator
    @staticmethod
    # Line 52: Definition of link_discord_account method
    # link_discord_account - link Discord account to user in DB
    # user_id: str - user ID in our system
    # discord_user: dict - Discord profile data (from fetch_discord_user)
    # -> dict - returns dictionary with linked Discord account data
    def link_discord_account(user_id: str, discord_user: dict) -> dict:
        # Line 53: Method docstring
        """
        Link Discord account to user in DB.
        """
        # Line 54: db - create DB session
        db: Session = SessionLocal()
        # Line 55: try - start of error handling block
        try:
            # Line 56: user - get user by ID
            user = UserRepository.get_by_id(db, user_id)

            # Line 57: if not user - check that user exists
            if not user:
                # Line 58: raise ValueError - user not found
                raise ValueError("User not found")

            # Line 59: discord_id - get Discord user ID
            # discord_user["id"] - required field (if missing - KeyError)
            discord_id = discord_user["id"]
            # Line 60: username - get Discord username
            # .get("username", "unknown") - safe retrieval (if missing - "unknown")
            username = discord_user.get("username", "unknown")
            # Line 61: discriminator - get discriminator (4 digits after #)
            # Old format: username#1234, new format Discord removed discriminator
            discriminator = discord_user.get("discriminator")
            # Line 62: avatar - get avatar hash
            avatar = discord_user.get("avatar")

            # Line 63: Comment about username format
            # Discord removed discriminator in new format
            # If discriminator exists and is not "0", use old format, otherwise only username
            # Line 64: if discriminator and discriminator != "0" - check old format
            if discriminator and discriminator != "0":
                # Line 65: discord_username - old format (username#1234)
                discord_username = f"{username}#{discriminator}"
            else:
                # Line 66: discord_username - new format (only username)
                discord_username = username

            # Line 67: avatar_url - form avatar URL
            # Ternary operator: value1 if condition else value2
            avatar_url = (
                # Line 68: if avatar exists, form URL
                # f"https://cdn.discordapp.com/avatars/{discord_id}/{avatar}.png" - URL template
                f"https://cdn.discordapp.com/avatars/{discord_id}/{avatar}.png"
                # Line 69: if avatar - condition (if avatar exists)
                if avatar
                # Line 70: else None - if avatar doesn't exist, return None
                else None
            )
            # CDN = Content Delivery Network - fast file distribution

            # Line 71: user.discord_id - save Discord ID to user object
            user.discord_id = discord_id
            # Line 72: user.discord_username - save username
            user.discord_username = discord_username
            # Line 73: user.discord_avatar_url - save avatar URL
            user.discord_avatar_url = avatar_url

            # Line 74: db.commit() - save changes to DB
            db.commit()
            # Line 75: db.refresh(user) - refresh object from DB
            db.refresh(user)

            # Line 76: return - return dictionary with Discord account data
            return {
                # Line 77: "discord_id": discord_id - Discord user ID
                "discord_id": discord_id,
                # Line 78: "discord_username": discord_username - username
                "discord_username": discord_username,
                # Line 79: "discord_avatar_url": avatar_url - avatar URL
                "discord_avatar_url": avatar_url,
            }
        # Line 80: except IntegrityError - catch DB integrity error
        # IntegrityError - occurs when DB constraints are violated (e.g., discord_id already used)
        except IntegrityError:
            # Line 81: db.rollback() - rollback changes (cancels commit)
            db.rollback()
            # Line 82: raise ValueError - raise understandable error
            raise ValueError("This Discord account is already linked to another user")
            # Why: one Discord account cannot be linked to multiple users
        # Line 83: finally - block that always executes (even on error)
        finally:
            # Line 84: db.close() - close DB session
            db.close()
            # Why: free connection resources

    # Line 85: @staticmethod decorator
    @staticmethod
    # Line 86: Definition of unlink_discord_account method
    # unlink_discord_account - unlink Discord account from user
    # user_id: str - user ID
    def unlink_discord_account(user_id: str):
        # Line 87: Method docstring
        """
        Unlink Discord account from user + attempt to remove role on server.
        """
        # Line 88: db - create DB session
        db: Session = SessionLocal()
        # Line 89: try - start of error handling block
        try:
            # Line 90: user - get user
            user = UserRepository.get_by_id(db, user_id)

            # Line 91: if not user - check existence
            if not user:
                # Line 92: raise ValueError - user not found
                raise ValueError("User not found")

            # Line 93: discord_id - save Discord ID before unlinking
            # Need to save to remove role on server later
            discord_id = user.discord_id

            # Line 94: user.discord_id = None - unlink Discord ID (set to None)
            user.discord_id = None
            # Line 95: user.discord_username = None - clear username
            user.discord_username = None
            # Line 96: user.discord_avatar_url = None - clear avatar URL
            user.discord_avatar_url = None

            # Line 97: db.commit() - save changes
            db.commit()
            # Line 98: db.refresh(user) - refresh object
            db.refresh(user)
        # Line 99: finally - block always executes
        finally:
            # Line 100: db.close() - close session
            db.close()

        # Line 101: if discord_id - check that Discord account was linked
        if discord_id:
            # Line 102: try - start of block for role removal
            try:
                # Line 103: remove_subscriber_role - attempt to remove subscriber role
                DiscordService.remove_subscriber_role(discord_id)
            # Line 104: except Exception - catch any errors
            except Exception as e:
                # Line 105: print - output error to console (temporary, better to use logger)
                print("Failed to remove Discord role on unlink:", e)
                # Why: don't let role removal error break account unlinking


    # Line 106: Comment - bot and server section
    # ---------- Bot / Guild helpers ----------
    # Bot = Discord bot (automated program)
    # Guild = Discord server/guild

    # Line 107: @staticmethod decorator
    @staticmethod
    # Line 108: Definition of private method _bot_headers
    # _bot_headers - form headers for requests on behalf of bot
    # Returns dictionary with Authorization header
    def _bot_headers():
        # Line 109: if not DISCORD_BOT_TOKEN - check that token is configured
        if not DISCORD_BOT_TOKEN:
            # Line 110: return {} - return empty dictionary if token is missing
            return {}
        # Line 111: return - return headers with bot token
        # "Authorization": f"Bot {DISCORD_BOT_TOKEN}" - bot token format (prefix "Bot ")
        return {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
        # Why: Discord API requires "Bot " prefix for bot tokens (difference from user tokens)

    # Line 112: @staticmethod decorator
    @staticmethod
    # Line 113: Definition of is_member_of_guild method
    # is_member_of_guild - check if user is member of server
    # discord_id: str - Discord user ID
    # -> bool - returns True if member, False if not
    def is_member_of_guild(discord_id: str) -> bool:
        # Line 114: Method docstring
        """
        Checks if user is member of required guild (server).
        Uses bot token.
        """
        # Line 115: if not DISCORD_GUILD_ID or not DISCORD_BOT_TOKEN - check settings
        if not DISCORD_GUILD_ID or not DISCORD_BOT_TOKEN:
            # Line 116: logger.warning - log warning
            logger.warning(
                "[DiscordService] GUILD_ID or BOT_TOKEN missing. Cannot verify guild membership."
            )
            # Line 117: return False - return False (cannot verify)
            return False

        # Line 118: url - form URL for membership check
        # f"{DISCORD_API}/guilds/{DISCORD_GUILD_ID}/members/{discord_id}" - API endpoint
        # /guilds/{id}/members/{id} - get server member information
        url = f"{DISCORD_API}/guilds/{DISCORD_GUILD_ID}/members/{discord_id}"

        # Line 119: with httpx.Client() - create HTTP client
        with httpx.Client(timeout=10.0) as client:
            # Line 120: r - GET request to check membership
            # client.get() - GET request
            # url - endpoint URL
            # headers=DiscordService._bot_headers() - headers with bot token
            r = client.get(url, headers=DiscordService._bot_headers())

        # Line 121: if r.status_code == 200 - check successful response
        if r.status_code == 200:
            # Line 122: return True - user is member of server
            return True
        # Line 123: if r.status_code == 404 - check that user not found
        if r.status_code == 404:
            # Line 124: return False - user is not member of server
            return False

        # Line 125: logger.error - log error for other statuses
        logger.error("Guild membership check failed: %s %s", r.status_code, r.text)
        # Line 126: return False - return False on error
        return False

    # Line 127: @staticmethod decorator
    @staticmethod
    # Line 128: Definition of user_has_subscriber_role method
    # user_has_subscriber_role - check if user has subscriber role
    # discord_id: str - Discord user ID
    # -> bool - returns True if has role, False if not
    def user_has_subscriber_role(discord_id: str) -> bool:
        # Line 129: Method docstring
        """
        Checks if user has subscriber role on server.
        """
        # Line 130: if - check that all necessary settings exist
        if (
            not DISCORD_GUILD_ID
            or not DISCORD_BOT_TOKEN
            or not DISCORD_SUBSCRIBER_ROLE_ID
        ):
            # Line 131: logger.warning - log warning
            logger.warning(
                "[DiscordService] GUILD_ID / BOT_TOKEN / ROLE_ID missing. Cannot verify roles."
            )
            # Line 132: return False - return False if settings incomplete
            return False

        # Line 133: url - form URL to get member information
        url = f"{DISCORD_API}/guilds/{DISCORD_GUILD_ID}/members/{discord_id}"

        # Line 134: with httpx.Client() - create HTTP client
        with httpx.Client(timeout=10.0) as client:
            # Line 135: r - GET request to get member data
            r = client.get(url, headers=DiscordService._bot_headers())

        # Line 136: if r.status_code == 404 - check that user not found
        if r.status_code == 404:
            # Line 137: return False - user not on server
            return False
        # Line 138: if r.status_code != 200 - check successful response
        if r.status_code != 200:
            # Line 139: logger.error - log error
            logger.error("Failed to fetch member for role check: %s %s", r.status_code, r.text)
            # Line 140: return False - return False on error
            return False

        # Line 141: data - get JSON from response
        data = r.json()
        # Line 142: roles - get list of user roles
        # data.get("roles", []) - safe retrieval (if missing - empty list)
        roles = data.get("roles", [])
        # Line 143: return - check that subscriber role is in list
        # str(DISCORD_SUBSCRIBER_ROLE_ID) in [str(rid) for rid in roles] - check presence
        # [str(rid) for rid in roles] - convert all role IDs to strings (list comprehension)
        # in - check membership (is our ID in the list)
        return str(DISCORD_SUBSCRIBER_ROLE_ID) in [str(rid) for rid in roles]
        # Why convert to strings: IDs can be numbers or strings, need to compare correctly


    # Line 144: Comment - roles section
    # ---------- Roles ----------

    # Line 145: @staticmethod decorator
    @staticmethod
    # Line 146: Definition of add_subscriber_role method
    # add_subscriber_role - grant subscriber role to user
    # discord_id: str - Discord user ID
    def add_subscriber_role(discord_id: str):
        # Line 147: Method docstring
        """
        Grant subscriber role on Discord server.
        """
        # Line 148: if not - check that all settings exist
        if not DISCORD_BOT_TOKEN or not DISCORD_GUILD_ID or not DISCORD_SUBSCRIBER_ROLE_ID:
            # Line 149: logger.warning - log warning
            logger.warning("Bot token or guild/role id missing — role not added.")
            # Line 150: return - exit without execution (early return)
            return

        # Line 151: url - form URL to grant role
        # f"{DISCORD_API}/guilds/{DISCORD_GUILD_ID}/members/{discord_id}/roles/{DISCORD_SUBSCRIBER_ROLE_ID}"
        # PUT request to this URL grants role to user
        url = (
            f"{DISCORD_API}/guilds/{DISCORD_GUILD_ID}/members/"
            f"{discord_id}/roles/{DISCORD_SUBSCRIBER_ROLE_ID}"
        )

        # Line 152: with httpx.Client() - create HTTP client
        with httpx.Client(timeout=10.0) as client:
            # Line 153: r - PUT request to grant role
            # client.put() - PUT request (update resource)
            # url - endpoint URL
            # headers=DiscordService._bot_headers() - headers with bot token
            r = client.put(url, headers=DiscordService._bot_headers())

        # Line 154: if r.status_code not in (204, 200) - check successful response
        # 204 = No Content (success without response body), 200 = OK (success with body)
        if r.status_code not in (204, 200):
            # Line 155: logger.error - log error
            logger.error("Failed to add role: %s %s", r.status_code, r.text)

    # Line 156: @staticmethod decorator
    @staticmethod
    # Line 157: Definition of remove_subscriber_role method
    # remove_subscriber_role - remove subscriber role from user
    # discord_id: str - Discord user ID
    def remove_subscriber_role(discord_id: str):
        # Line 158: Method docstring
        """
        Remove subscriber role from user on server.
        """
        # Line 159: if not - check settings
        if not DISCORD_BOT_TOKEN or not DISCORD_GUILD_ID or not DISCORD_SUBSCRIBER_ROLE_ID:
            # Line 160: logger.warning - log warning
            logger.warning("Bot token or guild/role id missing — role not removed.")
            # Line 161: return - exit without execution
            return

        # Line 162: url - form URL to remove role (same as for granting)
        url = (
            f"{DISCORD_API}/guilds/{DISCORD_GUILD_ID}/members/"
            f"{discord_id}/roles/{DISCORD_SUBSCRIBER_ROLE_ID}"
        )

        # Line 163: with httpx.Client() - create HTTP client
        with httpx.Client(timeout=10.0) as client:
            # Line 164: r - DELETE request to remove role
            # client.delete() - DELETE request (delete resource)
            # url - endpoint URL
            # headers=DiscordService._bot_headers() - headers with bot token
            r = client.delete(url, headers=DiscordService._bot_headers())

        # Line 165: if r.status_code not in (204, 200, 404) - check response
        # 404 = Not Found (role was already not granted, this is also success for us)
        if r.status_code not in (204, 200, 404):
            # Line 166: logger.error - log error
            logger.error("Failed to remove role: %s %s", r.status_code, r.text)


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 14:
# ==========================================================
# 
# 1. What is OAuth2 and how does authorization through Discord work?
#    What steps does user go through during authorization?
#
# 2. What is scope in OAuth2 and why is "identify" used?
#    What other scopes exist in Discord API?
#
# 3. What is state in OAuth2 and why is it needed?
#    What attack is protected against through state (CSRF)?
#
# 4. What's the difference between user access_token and bot token?
#    When is each one used?
#
# 5. What is IntegrityError and when does it occur?
#    Why do we do rollback() on IntegrityError?
#
# 6. Why do we need finally block in try/except/finally?
#    What will happen if we don't use finally to close session?
#
# 7. Why do we check status 404 as success when removing role?
#    What's the logic: "if role already doesn't exist - that's fine"?
#
# 8. What is discriminator in Discord and why can it be "0"?
#    How is discord_username formed in new and old format?
#
# 9. Why do we need private methods (with _ prefix) in Python?
#    Can we call _bot_headers() from outside the class?
#
# 10. How does role check through user_has_subscriber_role work?
#     Why do we need to convert IDs to strings when comparing?
#
# ==========================================================

