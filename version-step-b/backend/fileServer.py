from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

from controller import init_db
from controller.index import router

import redis.asyncio as redis
import uvicorn
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    redis_connection = redis.from_url("redis://localhost:6379", encoding="utf8")
    await FastAPILimiter.init(redis_connection)
    
    yield
    await FastAPILimiter.close()

    
app = FastAPI(lifespan=lifespan)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers['X-Content-Type-Options'] = 'nosniff'  # Prevents the browser from interpreting files as a different MIME type
        response.headers['X-Frame-Options'] = 'DENY' # Prevents clickjacking attacks
        response.headers['X-XSS-Protection'] = '1; mode=block' # Enables browser cross-site scripting filters
        # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload' # Forces HTTPS after the first request
       
        response.headers['Referrer-Policy'] = 'no-referrer' # Controls how much referrer information is sent with requests
        # response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; object-src 'none';" # Defines which dynamic resources are allowed to load
        response.headers['Permissions-Policy'] = "geolocation=(), microphone=(), camera=()" # A header for specifying the web features that the site wishes to use or not use
        return response


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Specify allowed origin |  allow_origins=["*"]
    allow_credentials=True,
    allow_methods=["GET", "POST"], # specify particular methods | allow_methods=["*"],
    allow_headers=["*"],
)


# Add the middleware to the app
app.add_middleware(SecurityHeadersMiddleware)

# Include the router
app.include_router(router)

