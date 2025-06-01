from fastapi import FastAPI, APIRouter, Request, Response
import httpx
from api_gateway_app.config import USER_SERVICE_URL

router = APIRouter()

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT"])
async def proxy_request(request: Request, path: str):
    url = f"{USER_SERVICE_URL}/{path}"
    method = request.method
    headers = dict(request.headers)
    body = await request.body()

    async with httpx.AsyncClient() as client:
        try:
            proxied_response = await client.request(
                method=method,
                url=url,
                headers=headers,
                content=body,
                timeout=10.0,
            )
        except httpx.RequestError as e:
            return Response(
                content=f"Service unavailable, {e}",
                status_code=502,
                media_type="text/plain"
            )

    return Response(
        content=proxied_response.content,
        status_code=proxied_response.status_code,
        headers=dict(proxied_response.headers),
        media_type=proxied_response.headers.get("content-type")
    )

def setup_proxy_routes(app: FastAPI):
    app.include_router(router)