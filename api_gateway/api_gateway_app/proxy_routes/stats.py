from fastapi import APIRouter, Query
from api_gateway_app.stats_grpc import stats_pb2
from api_gateway_app.stats_grpc.stats_client import get_stats_stub
from api_gateway_app.schemas import PostStatsResponse, DailyStatResponse, TopEntitiesResponse, DailyStatItem, TopEntityItem

router = APIRouter()

metric_map = {
    "view": stats_pb2.Metric.VIEW,
    "like": stats_pb2.Metric.LIKE,
    "comment": stats_pb2.Metric.COMMENT,
}
@router.get("/{post_id}", response_model=PostStatsResponse)
async def get_post_stats(post_id: int):
    stub = await get_stats_stub()
    request = stats_pb2.PostIdRequest(post_id=post_id)
    response = await stub.GetPostStats(request)
    return PostStatsResponse(
        views=response.views,
        likes=response.likes,
        comments=response.comments
    )

@router.get("/{post_id}/views", response_model=DailyStatResponse)
async def get_post_views(post_id: int):
    stub = await get_stats_stub()
    request = stats_pb2.PostIdRequest(post_id=post_id)
    response = await stub.GetPostViewsByDay(request)
    items = [DailyStatItem(date=item.date, count=item.count) for item in response.items]
    return DailyStatResponse(items=items)

@router.get("/{post_id}/likes", response_model=DailyStatResponse)
async def get_post_likes(post_id: int):
    stub = await get_stats_stub()
    request = stats_pb2.PostIdRequest(post_id=post_id)
    response = await stub.GetPostLikesByDay(request)
    items = [DailyStatItem(date=item.date, count=item.count) for item in response.items]
    return DailyStatResponse(items=items)

@router.get("/{post_id}/comments", response_model=DailyStatResponse)
async def get_post_comments(post_id: int):
    stub = await get_stats_stub()
    request = stats_pb2.PostIdRequest(post_id=post_id)
    response = await stub.GetPostCommentsByDay(request)
    items = [DailyStatItem(date=item.date, count=item.count) for item in response.items]
    return DailyStatResponse(items=items)

@router.get("/top/posts", response_model=TopEntitiesResponse)
async def get_top_posts(metric: str = Query(..., pattern="^(view|like|comment)$")):
    stub = await get_stats_stub()
    metric_enum = metric_map.get(metric)
    request = stats_pb2.TopRequest(metric=metric_enum)
    response = await stub.GetTopPostsBy(request)
    items = [TopEntityItem(id=item.id, count=item.count) for item in response.items]
    return TopEntitiesResponse(items=items)

@router.get("/top/users", response_model=TopEntitiesResponse)
async def get_top_users(metric: str = Query(..., pattern="^(view|like|comment)$")):
    stub = await get_stats_stub()
    metric_enum = metric_map.get(metric)
    request = stats_pb2.TopRequest(metric=metric_enum)
    response = await stub.GetTopUsersBy(request)
    items = [TopEntityItem(id=item.id, count=item.count) for item in response.items]
    return TopEntitiesResponse(items=items)