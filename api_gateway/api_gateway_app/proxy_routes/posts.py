import grpc
from fastapi import APIRouter, Depends, HTTPException, Query
from api_gateway_app.auth.dependencies import verify_token
from api_gateway_app.gateway_grpc.gateway_client import get_post_stub
from api_gateway_app.schemas import PostResponse, PostUpdate, PostCreate, PostListResponse, ListPosts
from api_gateway_app.gateway_grpc import post_pb2
from datetime import datetime

GRPC_TO_HTTP_STATUS = {
    grpc.StatusCode.OK: 200,
    grpc.StatusCode.INVALID_ARGUMENT: 422,
    grpc.StatusCode.NOT_FOUND: 404,
    grpc.StatusCode.ALREADY_EXISTS: 409,
    grpc.StatusCode.PERMISSION_DENIED: 403,
    grpc.StatusCode.UNAUTHENTICATED: 401,
    grpc.StatusCode.UNAVAILABLE: 503,
    grpc.StatusCode.DEADLINE_EXCEEDED: 504,
    grpc.StatusCode.INTERNAL: 500,
    grpc.StatusCode.UNKNOWN: 500,
}

router = APIRouter()

def grpc_to_pydantic(grpc_post: post_pb2.PostResponse) -> PostResponse:
    return PostResponse(
        id=grpc_post.id,
        title=grpc_post.title,
        description=grpc_post.description,
        creator_id=grpc_post.creator_id,
        created_at=datetime.fromisoformat(grpc_post.created_at),
        updated_at=datetime.fromisoformat(grpc_post.updated_at),
        is_private=grpc_post.is_private,
        tags=grpc_post.tags,
    )

@router.post("/create", response_model=PostResponse)
async def proxy_create_post(post_data: PostCreate, user_id: int = Depends(verify_token)):
    stub = await get_post_stub()
    try:
        grpc_response = await stub.CreatePost(
            post_pb2.CreatePostRequest(
                title=post_data.title,
                description=post_data.description,
                creator_id=user_id,
                is_private=post_data.is_private,
                tags=post_data.tags,
            )
        )
        return grpc_to_pydantic(grpc_response)
    except grpc.aio.AioRpcError as e:
        grpc_code = e.code()
        http_status = GRPC_TO_HTTP_STATUS.get(grpc_code, 502)
        print(f"[gRPC ERROR] code: {grpc_code} - details: {e.details()}")
        raise HTTPException(
            status_code=http_status,
            detail=f"Post service error: {grpc_code.name} - {e.details()}"
        )

@router.get("/{post_id}", response_model=PostResponse)
async def proxy_get_post(post_id: int, user_id: int = Depends(verify_token)):
    stub = await get_post_stub()
    try:
        grpc_response = await stub.GetPostById(post_pb2.GetPostRequest(id=post_id))
        if grpc_response.is_private and grpc_response.creator_id != user_id:
            raise HTTPException(status_code=403, detail="Access Denied")
        return grpc_to_pydantic(grpc_response)
    except grpc.aio.AioRpcError as e:
        grpc_code = e.code()
        http_status = GRPC_TO_HTTP_STATUS.get(grpc_code, 502)
        print(f"[gRPC ERROR] code: {grpc_code} - details: {e.details()}")
        raise HTTPException(
            status_code=http_status,
            detail=f"Post service error: {grpc_code.name} - {e.details()}"
        )

@router.put("/update/{post_id}", response_model=PostResponse)
async def proxy_update_post(post_id: int, update_data: PostUpdate, user_id: int = Depends(verify_token)):
    stub = await get_post_stub()
    try:
        grpc_response = await stub.UpdatePost(
            post_pb2.UpdatePostRequest(
                id=post_id,
                title=update_data.title,
                description=update_data.description,
                is_private=update_data.is_private,
                tags=update_data.tags,
                requestor_id=user_id,
            )
        )
        return grpc_to_pydantic(grpc_response)
    except grpc.aio.AioRpcError as e:
        grpc_code = e.code()
        http_status = GRPC_TO_HTTP_STATUS.get(grpc_code, 502)
        print(f"[gRPC ERROR] code: {grpc_code} - details: {e.details()}")
        raise HTTPException(
            status_code=http_status,
            detail=f"Post service error: {grpc_code.name} - {e.details()}"
        )

@router.delete("/delete/{post_id}")
async def proxy_delete_post(post_id: int, user_id: int = Depends(verify_token)):
    stub = await get_post_stub()
    try:
        grpc_response = await stub.DeletePost(
            post_pb2.DeletePostRequest(
                id=post_id,
                requestor_id=user_id,
            )
        )
        return
    except grpc.aio.AioRpcError as e:
        grpc_code = e.code()
        http_status = GRPC_TO_HTTP_STATUS.get(grpc_code, 502)
        print(f"[gRPC ERROR] code: {grpc_code} - details: {e.details()}")
        raise HTTPException(
            status_code=http_status,
            detail=f"Post service error: {grpc_code.name} - {e.details()}"
        )

@router.get("/list", response_model=PostListResponse)
async def proxy_list_posts(
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1),
        user_id: int = Depends(verify_token)):
    stub = await get_post_stub()
    try:
        grpc_response = await stub.ListPosts(
            post_pb2.ListPostsRequest(
                page=page,
                size=size
            )
        )
        posts = [grpc_to_pydantic(post) for post in grpc_response.posts]
        return PostListResponse(posts=posts, total=grpc_response.total)
    except grpc.aio.AioRpcError as e:
        grpc_code = e.code()
        http_status = GRPC_TO_HTTP_STATUS.get(grpc_code, 502)
        print(f"[gRPC ERROR] code: {grpc_code} - details: {e.details()}")
        raise HTTPException(
            status_code=http_status,
            detail=f"Post service error: {grpc_code.name} - {e.details()}"
        )