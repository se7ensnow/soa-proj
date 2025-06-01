import json

import httpx
from fastapi import APIRouter, Request, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from api_gateway_app.auth.dependencies import verify_token
from api_gateway_app.config import USER_SERVICE_URL

auth_router = APIRouter()

@auth_router.post("/register")
async def proxy_register(request: Request):
    try:
        body = await request.json()
    except json.decoder.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Missing or invalid JSON body")

    async with httpx.AsyncClient() as client:
        headers = {"Content-Type": "application/json"}
        response = await client.post(f"{USER_SERVICE_URL}/auth/register", json=body, headers=headers)
    return Response(status_code=response.status_code,
                    content=response.content,
                    headers=dict(response.headers),
                    media_type=response.headers.get("content-type")
                    )

@auth_router.post("/login")
async def proxy_login(form_data: OAuth2PasswordRequestForm = Depends()):
    async with httpx.AsyncClient() as client:
        body = {
            "username": form_data.username,
            "password": form_data.password
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = await client.post(f"{USER_SERVICE_URL}/auth/login", data=body, headers=headers)
    return Response(status_code=response.status_code,
                    content=response.content,
                    headers=dict(response.headers),
                    media_type=response.headers.get("content-type")
                    )

users_router = APIRouter()

@users_router.get("/{user_id}")
async def proxy_get_user(user_id: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{USER_SERVICE_URL}/users/{user_id}")
            return Response(status_code=response.status_code,
                            content=response.content,
                            headers=dict(response.headers),
                            media_type=response.headers.get("content-type")
                            )
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="User service unavailable")

@users_router.put("/update")
async def proxy_update_user(request: Request, user_id: int = Depends(verify_token)):
    try:
        body = await request.json()
    except json.decoder.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Missing or invalid JSON body")
    headers = {"Content-Type": "application/json", "Authorization": request.headers.get("Authorization")}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(
                f"{USER_SERVICE_URL}/users/{user_id}",
                json=body,
                headers=headers
            )
            return Response(status_code=response.status_code,
                            content=response.content,
                            headers=dict(response.headers),
                            media_type=response.headers.get("content-type")
                            )
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="User service unavailable")