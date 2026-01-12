# ==========================================================
# LESSON 22: MODULE 7 - CORE (Additional Components)
# middleware.py - Middleware for logging HTTP requests
# 
# This file contains the RequestLoggingMiddleware class for logging all HTTP requests
# to database and file. Middleware intercepts all API requests.
# ==========================================================

# Line 1: Comment with file path

# Line 2: Import time module for working with time
import time
# time.time() - get current time in seconds

# Line 3: Import Request from FastAPI
from fastapi import Request
# Request - HTTP request object

# Line 4: Import BaseHTTPMiddleware from Starlette
from starlette.middleware.base import BaseHTTPMiddleware
# BaseHTTPMiddleware - base class for creating middleware

# Line 5: Empty line for readability

# Line 6: Import log_action function from logger.py (lesson 18)
from app.core.logger import log_action
# Line 7: Import decode_access_token function from security.py (lesson 7)
from app.core.security import decode_access_token


# Line 8: Empty line for readability


# Line 9: Definition of RequestLoggingMiddleware class
# RequestLoggingMiddleware - middleware for logging requests
# BaseHTTPMiddleware - parent class (provides base functionality)
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    # Line 10: Class docstring
    """
    Logging each HTTP request + user_id if available.

    Uses AdminLog infrastructure (log_action) so all logs are
    in one place (admin_logs table + logs.txt file).
    """
    # Middleware = intermediate software that processes requests before/after handler
    # Logs all HTTP requests for monitoring and security

    # Line 11: Definition of dispatch method
    # async def dispatch() - asynchronous method called for each request
    # self - reference to class instance
    # request: Request - HTTP request object
    # call_next - function to pass request further along chain
    async def dispatch(self, request: Request, call_next):
        # Line 12: start_time - record request start time
        start_time = time.time()
        # time.time() - current time in seconds (Unix timestamp)
        # Why: need to calculate request execution time

        # Line 13: Comment - extract user_id from JWT
        # Try to extract user_id from JWT if Authorization header exists
        # Line 14: auth_header - get Authorization header
        auth_header = request.headers.get("Authorization")
        # .get() - safe header retrieval (returns None if missing)
        # Line 15: token - initialize variable for token
        token = None
        # Line 16: user_id - initialize variable for user ID
        user_id = None

        # Line 17: if auth_header and auth_header.startswith("Bearer ") - check header
        if auth_header and auth_header.startswith("Bearer "):
            # and - logical AND (both conditions must be True)
            # startswith("Bearer ") - check that header starts with "Bearer "
            # Line 18: token - extract token from header
            token = auth_header.split(" ", 1)[1].strip()
            # split(" ", 1) - split by first space
            # [1] - second element (token after "Bearer ")
            # strip() - remove whitespace

        # Line 19: if token - check that token exists
        if token:
            # Line 20: try - start of error handling block
            try:
                # Line 21: payload - decode token
                payload = decode_access_token(token)
                # decode_access_token() - function from security.py to decode JWT
                # Line 22: if isinstance(payload, dict) - check payload type
                if isinstance(payload, dict):
                    # isinstance() - function to check object type
                    # Line 23: user_id - get user ID from payload
                    user_id = payload.get("user_id")
            # Line 24: except Exception - catch any decoding errors
            except Exception:
                # Line 25: Comment - don't break main request
                # Don't let logging break main request
                # Line 26: user_id = None - set None on error
                user_id = None
                # Why: if couldn't decode token - just log without user_id

        # Line 27: Comment - execute request
        # Execute request
        # Line 28: response - pass request further along chain
        response = await call_next(request)
        # call_next() - function passes request to next middleware or handler
        # await - wait for result of asynchronous function
        # response - response from handler
        
        # Line 29: duration - calculate request execution time
        duration = round(time.time() - start_time, 4)
        # time.time() - start_time = time difference (in seconds)
        # round(..., 4) - round to 4 decimal places
        # Why: log execution time for performance analysis

        # Line 30: Comment - prepare data for logging
        # log_action expects admin_id (string) and details
        # Line 31: admin_id - set administrator ID (or "anonymous")
        admin_id = user_id or "anonymous"
        # Ternary operator via or: if user_id exists - use it, otherwise "anonymous"
        # Why: log_action requires string, cannot be None

        # Line 32: details - form string with request details
        details = (
            # Line 33: f"method={request.method}" - HTTP request method (GET, POST etc.)
            f"method={request.method}, "
            # Line 34: f"path={request.url.path}" - request path
            f"path={request.url.path}, "
            # Line 35: f"status={response.status_code}" - HTTP response status
            f"status={response.status_code}, "
            # Line 36: f"duration={duration}" - execution time in seconds
            f"duration={duration}"
        )
        # Multiline string in parentheses for readability

        # Line 37: try - start of block for logging
        try:
            # Line 38: log_action() - call logging function
            log_action(
                # Line 39: action="http_request" - action name
                action="http_request",
                # Line 40: admin_id=admin_id - user ID (or "anonymous")
                admin_id=admin_id,
                # Line 41: target_id=None - no action target (this is just request)
                target_id=None,
                # Line 42: details=details - request details
                details=details,
            )
        # Line 43: except Exception - catch logging errors
        except Exception:
            # Line 44: Comment - don't break application
            # Logging should not break application
            # Line 45: pass - ignore error
            pass
            # Why: if logging failed - not critical, continue work

        # Line 46: return response - return response to client
        return response
        # Middleware must return response so it reaches client


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 22:
# ==========================================================
# 
# 1. What is middleware in web applications?
#    How is middleware related to HTTP request processing?
#
# 2. Why log all HTTP requests?
#    What information is important for monitoring and security?
#
# 3. Why use await call_next(request)?
#    What's the difference between synchronous and asynchronous execution?
#
# 4. Why calculate duration (request execution time)?
#    How does this information help in performance analysis?
#
# 5. Why doesn't error handling when decoding token break request?
#    Why set user_id = None on error?
#
# 6. What does admin_id = user_id or "anonymous" mean?
#    How does or operator work with None and strings?
#
# 7. Why use try/except for log_action()?
#    Why shouldn't logging break main application?
#
# 8. What does isinstance(payload, dict) mean?
#    Why check payload type before using?
#
# 9. Why does middleware return response at end?
#    What will happen if we don't return response?
#
# 10. How is middleware related to other middleware in chain?
#     In what order are middleware executed in FastAPI?
#
# ==========================================================

