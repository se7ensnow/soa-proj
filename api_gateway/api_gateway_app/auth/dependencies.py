import httpx
from fastapi import Request, HTTPException, status

from api_gateway_app.config import USER_SERVICE_URL


async def verify_token(request: Request) -> int:
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    if not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header")

    token = auth_header.split(' ')[1]

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{USER_SERVICE_URL}/auth/verify", json={"access_token": token})
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="User service unavailable")

    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return int(response.json().get('user_id'))