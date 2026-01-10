# ==========================================================
# LESSON 20: MODULE 7 - CORE (Additional Components)
# dependencies.py - FastAPI Dependencies (Dependency Injection)
# 
# This file contains dependency functions for FastAPI, which are used
# for user authentication and authorization in endpoints.
# ==========================================================

# Line 1: Comment with file path

# Line 2: Import classes and functions from FastAPI
from fastapi import Depends, Header, HTTPException, status
# Depends - decorator for dependency injection
# Header - function to get HTTP request headers
# HTTPException - class for throwing HTTP exceptions (errors)
# status - module with HTTP status codes (200, 401, 403 etc.)

# Line 3: Empty line for readability

# Line 4: Import verify_access_token function from security.py (lesson 7)
from app.core.security import verify_access_token
# Line 5: Import UserService from user_service.py (lesson 11)
from app.services.user_service import UserService


# Line 6: Empty line for readability


# Line 7: Definition of get_current_user function
# get_current_user - dependency function to get current authorized user
# authorization: str = Header(None) - get Authorization header from HTTP request
# Header(None) - if header is missing, value will be None
def get_current_user(authorization: str = Header(None)):
    # Line 8: Function docstring
    """
    Extract token from Authorization header, decode JWT,
    get user_id and return dictionary with user.
    """
    # Dependency = dependency that is automatically called by FastAPI for endpoint
    
    # Line 9: if not authorization - check header presence
    if not authorization:
        # Line 10: raise HTTPException - throw HTTP exception
        # status_code=status.HTTP_401_UNAUTHORIZED - HTTP status 401 (unauthorized)
        # detail - error message for client
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Missing Authorization header")
        # Why: if header is missing - user is not authorized

    # Line 11: if not authorization.startswith("Bearer ") - check header format
    # startswith("Bearer ") - check that header starts with "Bearer "
    # Bearer - standard token format in HTTP header (OAuth2)
    if not authorization.startswith("Bearer "):
        # Line 12: raise HTTPException - throw exception on invalid format
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Authorization header format")
        # Why: header must be in format "Bearer <token>"

    # Line 13: token - extract token from header
    # authorization.split(" ", 1) - split string by first space
    # [1] - second element (index 1) - this is token (after "Bearer ")
    # .strip() - remove whitespace from edges
    token = authorization.split(" ", 1)[1].strip()
    # Example: "Bearer abc123" → split(" ", 1) → ["Bearer", "abc123"] → [1] → "abc123"
    
    # Line 14: payload - decode and verify token
    payload = verify_access_token(token)
    # verify_access_token() - function from security.py verifies token and returns data
    # If token is invalid or expired - function will throw HTTPException

    # Line 15: user_id - get user ID from token payload
    user_id = payload.get("user_id")
    # payload.get("user_id") - safe retrieval of "user_id" field from dictionary
    # Line 16: if not user_id - check that user_id exists
    if not user_id:
        # Line 17: raise HTTPException - throw exception if user_id is missing
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token payload")
        # Why: token must contain user_id

    # Line 18: user - get user data from DB
    user = UserService.get_user_by_id(user_id)
    # UserService.get_user_by_id() - service method to get user
    # Line 19: if not user - check that user is found
    if not user:
        # Line 20: raise HTTPException - throw exception if user not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
        # Why: if user is deleted from DB - token is invalid

    # Line 21: if user.get("status") == "banned" - check user status
    if user.get("status") == "banned":
        # Line 22: raise HTTPException - throw exception for banned user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is banned"
        )
        # HTTP 403 = Forbidden (access denied)
        # Why: banned users cannot use API

    # Line 23: return user - return dictionary with user data
    return user
    # FastAPI will automatically pass this dictionary to endpoint as parameter


# Line 24: Empty line for readability


# Line 25: Comment - admin dependencies section
# ---------- Admin / Superadmin ----------

# Line 26: Definition of require_admin function
# require_admin - dependency function to check administrator rights
# user=Depends(get_current_user) - dependency on get_current_user (first check authorization)
# Depends() - FastAPI decorator for dependency injection
def require_admin(user=Depends(get_current_user)):
    # Line 27: Function docstring
    """
    Check that user is admin (admin or superadmin).
    """
    # Line 28: if not user.get("is_admin", False) - check is_admin flag
    # user.get("is_admin", False) - safe flag retrieval (if missing - False)
    if not user.get("is_admin", False):
        # Line 29: raise HTTPException - throw exception if not admin
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Admin access required")
        # HTTP 403 = Forbidden (access denied)
    
    # Line 30: return user - return user if check passed
    return user

# Line 31: Empty line for readability

# Line 32: Definition of require_superadmin function
# require_superadmin - dependency function to check superadmin rights
def require_superadmin(user=Depends(get_current_user)):
    # Line 33: Function docstring
    """
    Check that user is specifically superadmin.
    """
    # Line 34: if user.get("role") != "superadmin" - check role
    if user.get("role") != "superadmin":
        # Line 35: raise HTTPException - throw exception if not superadmin
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Superadmin access required")
    
    # Line 36: return user - return user if check passed
    return user


# Line 37: Empty line for readability


# Line 38: Comment - aliases for backward compatibility
# ----- old names for full compatibility -----

# Line 39: get_current_admin_user - alias for require_admin
# Alias = different name for same function
get_current_admin_user = require_admin
# Line 40: get_current_superadmin_user - alias for require_superadmin
get_current_superadmin_user = require_superadmin
# Why: old code can use old names, they will work


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 20:
# ==========================================================
# 
# 1. What is Dependency Injection in FastAPI?
#    How does Depends() mechanism work?
#
# 2. What does Header(None) mean in function parameters?
#    How does FastAPI get HTTP request headers?
#
# 3. Why check Authorization header format (startswith("Bearer "))?
#    What will happen if token is passed in different format?
#
# 4. How does authorization.split(" ", 1)[1] work?
#    Why use [1] (second element), not [0]?
#
# 5. What's the difference between HTTP statuses 401 (Unauthorized) and 403 (Forbidden)?
#    When to use each?
#
# 6. Why check user.get("status") == "banned"?
#    What happens if banned user uses valid token?
#
# 7. How does Depends(get_current_user) work in require_admin function?
#    In what order are dependencies executed?
#
# 8. What's the difference between require_admin and require_superadmin?
#    Why for admin use is_admin, but for superadmin - role check?
#
# 9. Why do we need aliases (get_current_admin_user = require_admin)?
#    What is backward compatibility in programming?
#
# 10. Why does get_current_user function return dictionary, not User object?
#     What data should be in user dictionary?
#
# ==========================================================

