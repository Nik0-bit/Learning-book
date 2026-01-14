# ==========================================================
# LESSON 23: MODULE 7 - CORE (Additional Components)
# docs_security.py - Swagger documentation security
# 
# This file contains router and functions for secure access to Swagger UI
# documentation through API key and IP allowlist.
# ==========================================================

# Line 1: Comment with file path

# Line 2: Import classes and functions from FastAPI
from fastapi import APIRouter, Depends, Header, HTTPException, Request, Query
# APIRouter - class for creating router (group of endpoints)
# Depends - for dependency injection
# Header - for getting HTTP headers
# HTTPException - for throwing HTTP exceptions
# Request - HTTP request object
# Query - for getting query parameters from URL

# Line 3: Import functions for Swagger UI
from fastapi.openapi.docs import get_swagger_ui_html
# get_swagger_ui_html - function to generate Swagger UI HTML page

# Line 4: Import JSONResponse from FastAPI
from fastapi.responses import JSONResponse
# JSONResponse - class for creating JSON response

# Line 5: Import function to generate OpenAPI schema
from fastapi.openapi.utils import get_openapi
# get_openapi - function to generate OpenAPI schema (JSON API description)

# Line 6: Empty line for readability

# Line 7: Import constants from config.py (lesson 1)
from app.core.config import settings, DOCS_ALLOWED_IPS
# settings - settings object
# DOCS_ALLOWED_IPS - list of allowed IP addresses for documentation


# Line 8: router - create router object
router = APIRouter()
# APIRouter - router for grouping documentation endpoints
# Why: can connect all documentation endpoints with one app.include_router(router)


# Line 9: Empty line for readability


# Line 10: Definition of verify_docs_key function
# verify_docs_key - dependency function to check documentation access key
# x_docs_key: str = Header(None) - get key from X-Docs-Key header
# key: str = Query(None) - get key from query parameter (URL: ?key=...)
# request: Request = None - HTTP request object (to get IP)
def verify_docs_key(
    x_docs_key: str = Header(None),
    key: str = Query(None),
    request: Request = None,
):
    # Line 11: Function docstring
    """
    Check key and IP for documentation access.
    """
    # Why: protect documentation from unauthorized access
    
    # Line 12: required - get required key from settings
    required = settings.DOCS_API_KEY
    # settings.DOCS_API_KEY - key from configuration (must match passed key)

    # Line 13: if x_docs_key == required or key == required - check key
    # or - logical OR (one match is enough)
    # Key can be passed in header OR in query parameter
    if x_docs_key == required or key == required:
        # Line 14: Comment - check IP allowlist
        # IP allowlist, if set
        # Line 15: if DOCS_ALLOWED_IPS - check that allowlist is configured
        if DOCS_ALLOWED_IPS:
            # Line 16: allowed_ips - create set of allowed IPs
            # {ip.strip() for ip in DOCS_ALLOWED_IPS.split(",") if ip.strip()} - set comprehension
            # split(",") - split string by commas (list of IPs)
            # for ip in ... - iterate each IP
            # ip.strip() - remove whitespace
            # if ip.strip() - filter (skip empty strings)
            # {} - create set for fast lookup
            allowed_ips = {ip.strip() for ip in DOCS_ALLOWED_IPS.split(",") if ip.strip()}
            # Set = collection of unique elements, fast lookup via in
            
            # Line 17: client_ip - get client IP address
            client_ip = (
                # Line 18: get IP from X-Forwarded-For header (if proxy exists)
                request.headers.get("x-forwarded-for", "").split(",")[0].strip()
                # Line 19: or - if header missing, use IP from connection
                or (request.client.host if request.client else "")
                # request.client.host - IP address from direct connection
            )
            # Ternary operator via or: first try X-Forwarded-For, then request.client
            
            # Line 20: if allowed_ips and client_ip not in allowed_ips - check IP
            # allowed_ips - check that set is not empty
            # client_ip not in allowed_ips - check that IP is NOT in allowed list
            if allowed_ips and client_ip not in allowed_ips:
                # Line 21: raise HTTPException - throw exception on forbidden IP
                raise HTTPException(status_code=403, detail="Forbidden: IP not allowed")
                # HTTP 403 = Forbidden (access denied)
        
        # Line 22: return required - return key if check passed
        return required

    # Line 23: raise HTTPException - throw exception on invalid key
    raise HTTPException(status_code=403, detail="Forbidden: invalid docs key")
    # Why: if key doesn't match - access denied


# Line 24: @router.get() decorator - define GET endpoint
# "/docs" - endpoint path
# include_in_schema=False - don't include in OpenAPI schema (hide from documentation)
@router.get("/docs", include_in_schema=False)
# Line 25: Definition of async function custom_swagger_ui
# async def - asynchronous function
# docs_key: str = Depends(verify_docs_key) - dependency on verify_docs_key (key check)
async def custom_swagger_ui(docs_key: str = Depends(verify_docs_key)):
    # Line 26: Function docstring
    """
    Swagger UI + pass key for openapi.json.
    """
    # Swagger UI = web interface for testing API
    
    # Line 27: openapi_url - form URL for OpenAPI schema
    openapi_url = f"/openapi.json?key={docs_key}"
    # f-string to substitute docs_key in URL
    # Why: pass key in query parameter for access to openapi.json

    # Line 28: return - return Swagger UI HTML page
    return get_swagger_ui_html(
        # Line 29: title="Akiro Labs Backend API Docs" - page title
        title="Akiro Labs Backend API Docs",
        # Line 30: openapi_url=openapi_url - URL to load OpenAPI schema
        openapi_url=openapi_url,
        # Line 31: swagger_favicon_url - favicon URL
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        # Line 32: swagger_js_url - Swagger UI JavaScript file URL
        swagger_js_url="/static/swagger-ui-bundle.js",
        # Line 33: swagger_css_url - Swagger UI CSS file URL
        swagger_css_url="/static/swagger-ui.css",
        # Line 34: swagger_ui_parameters - Swagger UI configuration parameters
        swagger_ui_parameters={"persistAuthorization": True},
        # persistAuthorization=True - save authorization token between reloads
    )
    # Function generates HTML page with Swagger UI interface


# Line 35: Empty line for readability


# Line 36: @router.get() decorator - define GET endpoint
# "/openapi.json" - path to get OpenAPI schema
# include_in_schema=False - don't include in schema
@router.get("/openapi.json", include_in_schema=False)
# Line 37: Definition of async function custom_openapi
# request: Request - request object (needed to get routes)
# docs_key: str = Depends(verify_docs_key) - dependency on key check
async def custom_openapi(
    request: Request,
    docs_key: str = Depends(verify_docs_key)
):
    # Line 38: Function docstring
    """
    Custom OpenAPI with BearerAuth scheme added.
    """
    # OpenAPI = JSON API description schema (standard for documentation)
    
    # Line 39: openapi_schema - generate OpenAPI schema
    openapi_schema = get_openapi(
        # Line 40: title="Akiro Labs Backend" - API name
        title="Akiro Labs Backend",
        # Line 41: version="1.0.0" - API version
        version="1.0.0",
        # Line 42: routes=request.app.routes - list of all application routes
        routes=request.app.routes,
        # request.app - FastAPI application object
        # routes - list of all registered endpoints
    )
    # get_openapi() automatically generates schema based on application routes

    # Line 43: Comment - add BearerAuth scheme
    # ----------------------------
    # Add BearerAuth scheme
    # ----------------------------
    # Line 44: openapi_schema.setdefault("components", {}) - create components section
    # setdefault() - if key doesn't exist, creates it with value {}, if exists - returns existing
    openapi_schema.setdefault("components", {})
    # components - OpenAPI schema section for defining components (security schemes etc.)
    
    # Line 45: openapi_schema["components"].setdefault("securitySchemes", {}) - create securitySchemes
    openapi_schema["components"].setdefault("securitySchemes", {})
    # securitySchemes - subsection for security schemes (authorization types)
    
    # Line 46: openapi_schema["components"]["securitySchemes"]["BearerAuth"] - add BearerAuth
    openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
        # Line 47: "type": "http" - authorization type (HTTP)
        "type": "http",
        # Line 48: "scheme": "bearer" - authorization scheme (Bearer token)
        "scheme": "bearer",
        # Line 49: "bearerFormat": "JWT" - token format (JWT)
        "bearerFormat": "JWT"
    }
    # Why: define security scheme for Swagger UI (so can enter token)

    # Line 50: Comment - set BearerAuth as default
    # Make BearerAuth default scheme
    # Line 51: openapi_schema["security"] - set default security scheme
    openapi_schema["security"] = [{"BearerAuth": []}]
    # security - global OpenAPI section, defines default security schemes
    # [{"BearerAuth": []}] - list of schemes (BearerAuth applies to all endpoints)
    # Why: all endpoints by default require Bearer token (can override in specific endpoint)

    # Line 52: return JSONResponse(openapi_schema) - return JSON schema
    return JSONResponse(openapi_schema)
    # JSONResponse - class for creating JSON response with correct headers
    # openapi_schema - Python dictionary automatically converted to JSON


# ==========================================================
# QUESTIONS FOR REINFORCING LESSON 23:
# ==========================================================
# 
# 1. Why protect Swagger documentation with key?
#    What security risks arise with public documentation?
#
# 2. What is OpenAPI schema and why is it needed?
#    How does Swagger UI use OpenAPI schema?
#
# 3. Why check IP address (IP allowlist)?
#    In what cases is this useful for security?
#
# 4. How does set comprehension {x for x in items} work?
#    What are advantages of set over list for in check?
#
# 5. Why use setdefault() to create nested dictionaries?
#    What will happen if we use regular assignment?
#
# 6. What does "BearerAuth" mean in OpenAPI schema?
#    How does Swagger UI use this scheme for authorization?
#
# 7. Why set security as default for all endpoints?
#    Can we override security scheme for specific endpoint?
#
# 8. What does include_in_schema=False mean?
#    Why hide documentation endpoints from documentation itself?
#
# 9. How does key check work through Header OR Query parameter?
#    Why support both ways of passing key?
#
# 10. What is JSONResponse and how does it differ from regular return dictionary?
#     What headers does JSONResponse add?
#
# ==========================================================

