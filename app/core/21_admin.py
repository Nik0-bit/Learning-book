# ==========================================================
# LESSON 21: MODULE 7 - CORE (Additional Components)
# admin.py - Additional dependencies for admin panel
# 
# This file contains the admin_required function for checking administrator rights
# in admin panel endpoints. Alternative dependency option for admins.
# ==========================================================

# Line 1: Empty line (in original file starts with empty line)

# Line 2: Import classes from FastAPI
from fastapi import Depends, HTTPException, status
# Depends - for dependency injection
# HTTPException - for throwing HTTP exceptions
# status - module with HTTP status codes

# Line 3: Empty line for readability

# Line 4: Import get_current_user function from dependencies.py (lesson 20)
from app.core.dependencies import get_current_user


# Line 5: Empty line for readability


# Line 6: Definition of admin_required function
# admin_required - dependency function to check administrator rights
# current_user=Depends(get_current_user) - dependency on get_current_user
# First check authorization, then administrator rights
def admin_required(current_user=Depends(get_current_user)):
    # Line 7: Function docstring
    """
    Dependency for admin panel endpoints.
    Allows only if user has 'admin' role.
    """
    # Dependency = FastAPI dependency, automatically called for endpoint
    
    # Line 8: if current_user.get("role") not in ("admin", "superadmin") - check role
    # current_user.get("role") - get user role
    # not in ("admin", "superadmin") - check that role is NOT in list of admin roles
    # in - operator to check element membership in collection
    if current_user.get("role") not in ("admin", "superadmin"):
        # Line 9: raise HTTPException - throw HTTP exception
        raise HTTPException(
            # Line 10: status_code=status.HTTP_403_FORBIDDEN - HTTP status 403
            status_code=status.HTTP_403_FORBIDDEN,
            # HTTP 403 = Forbidden (access denied)
            # Line 11: detail - error message
            detail="Admin access required",
        )
        # Why: only admins and superadmins can use admin panel
    
    # Line 12: return current_user - return user if check passed
    return current_user
    # FastAPI will pass current_user to endpoint as parameter


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 21:
# ==========================================================
# 
# 1. What's the difference between admin_required and require_admin from dependencies.py?
#    Why are there two ways to check administrator rights?
#
# 2. How does not in operator work for role check?
#    What does current_user.get("role") not in ("admin", "superadmin") mean?
#
# 3. Why check role through get("role"), not through is_admin?
#    What's the difference between these approaches?
#
# 4. Why do we need Depends(get_current_user) in function parameters?
#    In what order are dependencies executed?
#
# 5. Why is function called admin_required, not require_admin?
#    Is there any difference in usage?
#
# ==========================================================

