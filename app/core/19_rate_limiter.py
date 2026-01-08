# ==========================================================
# LESSON 19: MODULE 7 - CORE (Additional Components)
# rate_limiter.py - Request Rate Limiting
# 
# This file contains the RateLimitMiddleware class for protecting API from abuse
# (DDoS attacks, password brute force etc.) through limiting number of requests.
# ==========================================================

# Line 1: Import time module for working with time
import time
# time.time() - get current time in seconds (Unix timestamp)

# Line 2: Import types from typing module
from typing import Dict, Tuple, List, Optional
# Dict - dictionary (key-value)
# Tuple - tuple (immutable list)
# List - list
# Optional - optional type (can be None)

# Line 3: Empty line for readability

# Line 4: Import BaseHTTPMiddleware from Starlette
# From where: Starlette library (used by FastAPI)
# BaseHTTPMiddleware - base class for creating middleware
from starlette.middleware.base import BaseHTTPMiddleware
# Comparison: BaseHTTPMiddleware = like template for creating guard (middleware)

# Line 5: Import Request from Starlette
from starlette.requests import Request
# Request - HTTP request object (method, path, headers etc.)

# Line 6: Import Response from Starlette
from starlette.responses import Response
# Response - HTTP response object (status, body etc.)

# Line 7: Empty line for readability

# Line 8: Import constants from config.py (lesson 1)
from app.core.config import (
    # RATE_LIMIT_AUTH_PER_MINUTE - limit for authorization endpoints
    RATE_LIMIT_AUTH_PER_MINUTE,
    # RATE_LIMIT_DISCORD_PER_MINUTE - limit for Discord endpoints
    RATE_LIMIT_DISCORD_PER_MINUTE,
    # RATE_LIMIT_ADMIN_PER_MINUTE - limit for admin endpoints
    RATE_LIMIT_ADMIN_PER_MINUTE,
    # RATE_LIMIT_DOCS_PER_MINUTE - limit for documentation
    RATE_LIMIT_DOCS_PER_MINUTE,
)


# Line 9: Empty line for readability


# Line 10: Comment - storing limit state
# Store limit state in process memory
# key: (ip, scope) -> list[timestamps]
# Line 11: RateStore - type for storing request data
# Dict[Tuple[str, str], List[float]] - dictionary where:
# Key: tuple (IP address, scope) - (str, str)
# Value: list of request timestamps - List[float]
RateStore = Dict[Tuple[str, str], List[float]]
# Comparison: RateStore = like visit log - record who and when made requests

# Line 12: _rate_store - global variable for storing data
# RateStore = {} - empty dictionary (initial state)
# Prefix _ means variable is private (internal)
_rate_store: RateStore = {}
# Why: store request data in memory (to count number of requests per period)


# Line 13: Empty line for readability


# Line 14: Definition of RateLimitMiddleware class
# class RateLimitMiddleware(BaseHTTPMiddleware): - create middleware class
# BaseHTTPMiddleware - parent class (provides base functionality)
class RateLimitMiddleware(BaseHTTPMiddleware):
    # Line 15: Class docstring
    """
    Simple in-memory rate limiter.

    Limits:
      - /auth/*     → RATE_LIMIT_AUTH_PER_MINUTE requests per minute
      - /discord/*  → RATE_LIMIT_DISCORD_PER_MINUTE
      - /admin/*    → RATE_LIMIT_ADMIN_PER_MINUTE

    Other routes are not affected.
    """
    # in-memory = in memory (data is not saved to DB, lost on restart)
    # Rate limiter = request frequency limiter (protection against abuse)

    # Line 16: Definition of dispatch method
    # async def dispatch() - asynchronous method called for each request
    # self - reference to class instance
    # request: Request - HTTP request object
    # call_next - function to pass request further along middleware chain
    async def dispatch(self, request: Request, call_next):
        # Line 17: path - get request path
        path = request.url.path
        # request.url.path - URL path (e.g., "/auth/login", "/admin/users")
        
        # Line 18: scope - determine scope for this path
        scope = self._match_scope(path)
        # _match_scope() - private method to determine which limit to apply

        # Line 19: Comment - check if path is under limit
        # If path is not under limit — just pass through
        # Line 20: if scope is None - check that path is not under limit
        if scope is None:
            # Line 21: return - pass request further without restrictions
            return await call_next(request)
            # await - wait for result of asynchronous function
            # If path is not under limit - just pass request through

        # Line 22: scope_name, limit, window - unpack scope tuple
        # Unpacking = assign tuple elements to variables
        scope_name, limit, window = scope
        # scope_name - scope name ("auth", "discord", "admin", "docs")
        # limit - maximum number of requests (e.g., 20)
        # window - time window in seconds (60.0 = 1 minute)
        
        # Line 23: client_ip - get client IP address
        client_ip = self._get_client_ip(request)
        # _get_client_ip() - private method to get IP
        
        # Line 24: key - form key for dictionary
        key = (client_ip, scope_name)
        # Tuple (IP, scope) = unique key for each client and each scope
        # Example: ("192.168.1.1", "auth")

        # Line 25: now - current time in seconds
        now = time.time()
        # time.time() - Unix timestamp (number of seconds since January 1, 1970)

        # Line 26: Comment - get past timestamps
        # Get past timestamps
        # Line 27: timestamps - get list of timestamps for this key
        # _rate_store.get(key, []) - get list of timestamps or empty list if key doesn't exist
        timestamps = _rate_store.get(key, [])
        # timestamps = list of times when previous requests were made

        # Line 28: Comment - clean old timestamps
        # Clean those older than window
        # Line 29: timestamps - filter timestamps (list comprehension)
        # [element for element in list if condition] - list generator with condition
        timestamps = [ts for ts in timestamps if now - ts < window]
        # now - ts < window - check that timestamp is within time window
        # If now - ts >= window - timestamp is older than window, remove it
        # Example: if now is 100, window=60, then timestamp 30 will be removed (100-30=70 > 60)
        # Comparison: like cleaning old records - remove everything older than minute

        # Line 30: Comment - check limit
        # Check limit
        # Line 31: if len(timestamps) >= limit - check limit exceeded
        if len(timestamps) >= limit:
            # len(timestamps) - number of requests in window
            # >= limit - if requests are greater or equal to limit - block
            # Line 32: Comment - can add Retry-After
            # Can add Retry-After if you want
            # Line 33: return Response() - return "Too Many Requests" response
            return Response(
                # Line 34: content - response body (JSON string)
                content='{"detail":"Too Many Requests"}',
                # Line 35: status_code=429 - HTTP status "Too Many Requests"
                status_code=429,
                # 429 - standard code for request limit exceeded
                # Line 36: media_type="application/json" - content type (JSON)
                media_type="application/json",
            )
            # Why: block request, return 429 error

        # Line 37: Comment - add current request
        # Add current request and save
        # Line 38: timestamps.append(now) - add current timestamp
        timestamps.append(now)
        # append() - list method to add element to end
        # Line 39: _rate_store[key] = timestamps - save updated list
        _rate_store[key] = timestamps
        # Why: save request history for future checks

        # Line 40: Comment - pass request further
        # Pass through
        # Line 41: response - pass request further along chain
        response = await call_next(request)
        # call_next() - function passes request to next middleware or handler
        # Line 42: return response - return response to client
        return response

    # Line 43: @staticmethod decorator
    @staticmethod
    # Line 44: Definition of private method _get_client_ip
    # _get_client_ip - get client IP address from request
    # request: Request - HTTP request object
    # -> str - returns string with IP address
    def _get_client_ip(request: Request) -> str:
        # Line 45: Comment about proxy
        # If behind proxy (nginx), can use X-Forwarded-For
        # X-Forwarded-For - HTTP header for passing real IP through proxy
        # Line 46: xff - get X-Forwarded-For header
        xff = request.headers.get("x-forwarded-for")
        # .get() - safe header retrieval (returns None if missing)
        # Line 47: if xff - check that header exists
        if xff:
            # Line 48: return - return first IP from list
            return xff.split(",")[0].strip()
            # split(",") - split string by comma (can be multiple IPs)
            # [0] - first element of list (real client IP)
            # strip() - remove whitespace from edges
            # Why: if request goes through proxy, real IP is in X-Forwarded-For

        # Line 49: client - get client connection directly
        client = request.client
        # request.client - client connection information (if no proxy)
        # Line 50: return - return IP from connection or "unknown"
        return client.host if client else "unknown"
        # Ternary operator: if client exists - return client.host, otherwise "unknown"
        # Why: safe check in case client information is missing

    # Line 51: @staticmethod decorator
    @staticmethod
    # Line 52: Definition of private method _match_scope
    # _match_scope - determine scope for request path
    # path: str - request path (e.g., "/auth/login")
    # -> Optional[Tuple[str, int, float]] - returns tuple or None
    def _match_scope(path: str) -> Optional[Tuple[str, int, float]]:
        # Line 53: Method docstring
        """
        Returns (scope_name, limit, window_seconds) or None if path is not interesting.
        """
        # scope_name - scope name ("auth", "discord" etc.)
        # limit - maximum number of requests
        # window_seconds - time window in seconds
        
        # Line 54: if path.startswith("/auth") - check path start
        if path.startswith("/auth"):
            # startswith() - string method to check string start
            # Line 55: return - return tuple for auth scope
            return ("auth", RATE_LIMIT_AUTH_PER_MINUTE, 60.0)
            # ("auth", 20, 60.0) - scope="auth", limit=20 requests, window=60 seconds
        
        # Line 56: if path.startswith("/discord") - check for Discord
        if path.startswith("/discord"):
            # Line 57: return - return tuple for discord scope
            return ("discord", RATE_LIMIT_DISCORD_PER_MINUTE, 60.0)
        
        # Line 58: if path.startswith("/admin") - check for admin endpoints
        if path.startswith("/admin"):
            # Line 59: return - return tuple for admin scope
            return ("admin", RATE_LIMIT_ADMIN_PER_MINUTE, 60.0)
        
        # Line 60: if path.startswith("/docs") or path.startswith("/openapi") - check for documentation
        if path.startswith("/docs") or path.startswith("/openapi"):
            # or - logical OR (at least one condition must be True)
            # Line 61: return - return tuple for docs scope
            return ("docs", RATE_LIMIT_DOCS_PER_MINUTE, 60.0)

        # Line 62: return None - return None if path doesn't match
        return None
        # Why: if path doesn't match any scope - limit is not applied


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 19:
# ==========================================================
# 
# 1. What is rate limiting and why is it needed?
#    What attacks does rate limiter protect against?
#
# 2. What does "in-memory" data storage mean?
#    What problems can arise when storing in memory?
#
# 3. What is sliding window algorithm?
#    How does cleaning old timestamps work?
#
# 4. Why do we need key (client_ip, scope_name) for dictionary?
#    Why use tuple instead of just IP address?
#
# 5. What does HTTP status code 429 mean?
#    In what other situations is this code returned?
#
# 6. Why do we need X-Forwarded-For header?
#    Why when working behind proxy need to use it instead of request.client?
#
# 7. How does startswith() method work for strings?
#    Why use startswith() instead of exact path comparison?
#
# 8. What happens when server restarts with _rate_store?
#    What data is lost and why?
#
# 9. Why use await call_next(request)?
#    What is asynchronicity and why is it needed in FastAPI?
#
# 10. Why different limits for different scopes (auth, admin, discord)?
#     Why is limit lower for admin endpoints?
#
# ==========================================================

