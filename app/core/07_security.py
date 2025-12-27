# ==========================================================
# LESSON 7: MODULE 4 - CORE (Security)
# security.py - JWT Token Handling
# 
# This file contains functions for creating and verifying JWT (JSON Web Token) tokens.
# JWT tokens are used for user authentication without storing sessions on server.
# ==========================================================

# Line 1: Comment with file path

# Line 2: Import datetime and timedelta classes from datetime module
# From where: built-in Python module
# datetime - class for working with date and time
# timedelta - class for working with time intervals (adding/subtracting time)
from datetime import datetime, timedelta
# Analogy: datetime = calendar (shows date/time), timedelta = timer (time interval)
# Why timedelta: need to add 60 minutes to current time for token expiration


# Line 3: Empty line for readability


# Line 4: Import HTTPException from FastAPI
# From where: external FastAPI library (pip install fastapi)
# HTTPException - class for raising HTTP errors (400, 401, 500, etc.)
from fastapi import HTTPException
# Why: when errors occur creating/verifying token need to return correct HTTP status code


# Line 5: Import functions and exceptions from jose library
# From where: external python-jose library (pip install python-jose[cryptography])
# What is this: library for working with JWT tokens
# jwt - module for working with JWT (encoding/decoding)
# JWTError - general exception for JWT errors
# ExpiredSignatureError - specific exception for expired token
from jose import jwt, JWTError, ExpiredSignatureError
# Analogy: jose = like tool for working with passes (creation and verification)
# JWTError = general error (pass damaged), ExpiredSignatureError = specific error (pass expired)


# Line 6: Import constants from config.py (lesson 1)
# SECRET_KEY - secret key for signing tokens
# ACCESS_TOKEN_EXPIRE_MINUTES - token lifetime in minutes
from app.core.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
# Why import from config: use settings from configuration (don't hardcode values)


# Line 7: Empty line for readability


# Line 8: ALGORITHM - encryption algorithm for JWT
# "HS256" - HMAC-SHA256 algorithm (symmetric encryption)
# HMAC = Hash-based Message Authentication Code (message authentication code based on hash)
# SHA256 = hashing algorithm (256 bits)
# Symmetric = one key for encryption and decryption (SECRET_KEY)
ALGORITHM = "HS256"
# Analogy: algorithm = like way to sign document (pen signature, stamp, electronic signature)
# HS256 = like stamp with secret code - only one who knows code can verify signature


# Line 9: Empty line for readability


# Line 10: Definition of create_access_token function
# def - keyword for creating function
# create_access_token - function name (creating access token)
# data: dict - function parameter, data type dict (dictionary)
# -> str - return type annotation (function returns string)
# data contains information to encode in token (e.g., {"user_id": "123"})
def create_access_token(data: dict) -> str:
    # Line 11: Triple quotes - docstring (function documentation)
    # Docstring = documentation string describing what function does
    """
    Creates JWT token.
    """
    # Line 12: to_encode - copy of data dictionary
    # data.copy() - creates copy of dictionary (not reference to original)
    # Why copy: to avoid modifying original data dictionary when adding "exp" field
    to_encode = data.copy()
    # Analogy: copy() = like photocopying document - you modify copy, original doesn't change
    
    # Line 13: expire - token expiration date and time
    # datetime.utcnow() - current time in UTC (Coordinated Universal Time)
    # timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) - time interval (e.g., 60 minutes)
    # + - adding date and interval = get date after specified time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Example: if now 10:00, ACCESS_TOKEN_EXPIRE_MINUTES=60, then expire = 11:00
    # Analogy: like pass expiration date - issued for specific time (e.g., one hour)
    
    # Line 14: to_encode.update() - adding "exp" field to dictionary
    # {"exp": expire} - dictionary with one key "exp" (expiration)
    # update() - dictionary method for adding/updating keys
    # "exp" - standard JWT field for token expiration time
    to_encode.update({"exp": expire})
    # Why: JWT standard requires "exp" field for determining token expiration
    
    # Line 15: Empty line for readability
    
    # Line 16: try - start of exception handling block
    # try/except - construct for catching errors (if something goes wrong)
    try:
        # Line 17: token - creating JWT token
        # jwt.encode() - function from jose library for encoding data into JWT token
        # to_encode - data to encode (dictionary with information and expiration time)
        # SECRET_KEY - secret key for signing token (from config.py)
        # algorithm=ALGORITHM - encryption algorithm (HS256)
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        # What happens: data encoded into string and signed with secret key
        # Result: string like "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." (encrypted data)
        # Analogy: like sealing envelope with document - document (data) + seal (SECRET_KEY)
        
        # Line 18: return token - return created token
        # return - keyword for returning value from function
        return token
        # Function ends here if everything went successfully
        
    # Line 19: except Exception as e - catch any exceptions
    # except - block that executes if error occurred in try
    # Exception - base class for all Python exceptions
    # as e - save exception object to variable e (to know what went wrong)
    except Exception as e:
        # Line 20: raise HTTPException - raise HTTP exception
        # raise - keyword for raising exception
        # HTTPException - class from FastAPI for HTTP errors
        # status_code=500 - HTTP status code 500 (Internal Server Error)
        # detail=f"Token creation error: {e}" - error message (f-string for variable substitution)
        raise HTTPException(status_code=500, detail=f"Token creation error: {e}")
        # Why: if failed to create token, return 500 error to client
        # f-string: f"text {variable}" - string with variable substitution


# Line 21: Empty line for readability


# Line 22: Definition of verify_access_token function
# verify_access_token - verify and decode JWT token
# token: str - function parameter, type str (string with token)
# -> dict - function returns dictionary (decoded data from token)
def verify_access_token(token: str) -> dict:
    # Line 23: Function docstring
    """
    Decodes and validates JWT token.
    """
    # Line 24: try - start of exception handling block
    try:
        # Line 25: payload - decode token
        # jwt.decode() - function for decoding JWT token
        # token - string with token to decode
        # SECRET_KEY - secret key for verifying signature (must match key used when creating)
        # algorithms=[ALGORITHM] - list of allowed algorithms (for security, don't accept other algorithms)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # What happens: token decoded, SECRET_KEY signature verified, data returned
        # payload = dictionary with data from token (e.g., {"user_id": "123", "exp": 1234567890})
        # Analogy: like pass verification - signature/stamp checked, then contents read
        
        # Line 26: return payload - return decoded data
        return payload
        # If token valid (correct signature, not expired), return data
        
    # Line 27: except ExpiredSignatureError - catch expired token exception
    # ExpiredSignatureError - specific exception from jose for expired tokens
    # This happens if "exp" field in token points to past time
    except ExpiredSignatureError:
        # Line 28: Raise HTTP error 401 (Unauthorized)
        # 401 - standard code for unauthorized requests (token expired = need to re-authenticate)
        raise HTTPException(status_code=401, detail="Token expired")
        # Analogy: like pass with expired validity - won't let through, need to get new one
        
    # Line 29: except JWTError - catch other JWT errors
    # JWTError - general class for all JWT errors (wrong signature, invalid format, etc.)
    # This block triggers for any other errors (except expired token)
    except JWTError:
        # Line 30: Raise HTTP error 401 with message "Invalid token"
        raise HTTPException(status_code=401, detail="Invalid token")
        # Analogy: like fake pass - signature doesn't match, access denied


# Line 31: Empty line for readability


# Line 32: Comment - alias for backward compatibility
# Alias = different name for same function
# Why: possibly old code used name decode_access_token

# ---- alias for old code ----
# Line 33: Definition of decode_access_token function
# decode_access_token - old function name (for backward compatibility)
def decode_access_token(token: str) -> dict:
    # Line 34: Function docstring
    """
    Old function name. For backward compatibility.
    """
    # Line 35: return verify_access_token(token) - call new function
    # Function simply calls verify_access_token and returns its result
    # This allows old code to continue working using old name
    return verify_access_token(token)
    # Analogy: like synonym - two different names, but mean the same thing


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 7:
# ==========================================================
# 
# 1. What is JWT token and why is it needed?
#    What's the difference between JWT and regular server sessions?
#
# 2. What does SECRET_KEY mean and why must it be secret?
#    What will happen if someone finds out SECRET_KEY?
#
# 3. What is HS256 algorithm and why is it called symmetric?
#    What's the difference between symmetric and asymmetric encryption?
#
# 4. Why is data.copy() function needed in create_access_token?
#    What will happen if use data directly instead of copy?
#
# 5. What does "exp" field in JWT token mean?
#    How does system check that token expired?
#
# 6. What is try/except and why is exception handling needed?
#    What errors can occur when creating token?
#
# 7. What's the difference between ExpiredSignatureError and JWTError?
#    Why do they return different error messages?
#
# 8. What does HTTP status code 401 (Unauthorized) mean?
#    When is 401 used, and when 403 (Forbidden)?
#
# 9. Why is algorithms=[ALGORITHM] parameter needed in jwt.decode()?
#    What vulnerability can arise if don't specify algorithms?
#
# 10. Why is decode_access_token function needed if it just calls verify_access_token?
#     What is backward compatibility in programming?
#
# ==========================================================
