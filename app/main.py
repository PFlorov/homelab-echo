import os
import socket
from datetime import datetime, timezone

from fastapi import FastAPI, Request

app = FastAPI()


def get_app_info():
    return {
        "app_name": os.getenv("APP_NAME", "homelab-echo"),
        "environment": os.getenv("APP_ENV", "dev"),
        "version": os.getenv("APP_VERSION", "unknown"),
        "hostname": socket.gethostname(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/")
def root():
    return {
        "message": "Hello from homelab-echo",
        **get_app_info(),
    }


@app.get("/healthz")
def healthz():
    return {
        "status": "ok",
        **get_app_info(),
    }


@app.get("/env")
def env():
    return {
        "app_name": os.getenv("APP_NAME", "homelab-echo"),
        "environment": os.getenv("APP_ENV", "dev"),
        "version": os.getenv("APP_VERSION", "unknown"),
    }


@app.get("/headers")
async def headers(request: Request):
    return {
        "headers": dict(request.headers),
        **get_app_info(),
    }


@app.get("/info")
async def info(request: Request):
    client_host = request.client.host if request.client else "unknown"

    return {
        "message": "Detailed request info",
        **get_app_info(),
        "client_host": client_host,
        "method": request.method,
        "url": str(request.url),
        "base_url": str(request.base_url),
        "path": request.url.path,
        "query_params": dict(request.query_params),
        "headers": dict(request.headers),
    }
