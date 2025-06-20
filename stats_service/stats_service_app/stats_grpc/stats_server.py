import grpc

from stats_service_app.stats_grpc import stats_pb2_grpc, stats_pb2
from stats_service_app.database import clickhouse_client
from stats_service_app.crud import get_post_stats, get_post_metric_by_day, get_top_posts_by, get_top_users_by

metric_map = {
    stats_pb2.Metric.VIEW: "view",
    stats_pb2.Metric.LIKE: "like",
    stats_pb2.Metric.COMMENT: "comment"
}

class StatsService(stats_pb2_grpc.StatsServiceServicer):
    def GetPostStats(self, request, context):
        post_id = request.post_id
        stats = get_post_stats(clickhouse_client, post_id)
        return stats_pb2.PostStatSummary(
            views=stats['views'],
            likes=stats['likes'],
            comments=stats['comments']
        )

    def GetPostViewsByDay(self, request, context):
        post_id = request.post_id
        rows = get_post_metric_by_day(clickhouse_client, post_id, metric='view')
        return stats_pb2.DailyStatResponse(
            items=[stats_pb2.DailyStat(date=str(r["date"]), count=r["count"]) for r in rows]
        )

    def GetPostLikesByDay(self, request, context):
        post_id = request.post_id
        rows = get_post_metric_by_day(clickhouse_client, post_id, metric='like')
        return stats_pb2.DailyStatResponse(
            items=[stats_pb2.DailyStat(date=str(r["date"]), count=r["count"]) for r in rows]
        )

    def GetPostCommentsByDay(self, request, context):
        post_id = request.post_id
        rows = get_post_metric_by_day(clickhouse_client, post_id, metric='comment')
        return stats_pb2.DailyStatResponse(
            items=[stats_pb2.DailyStat(date=str(r["date"]), count=r["count"]) for r in rows]
        )

    def GetTopPostsBy(self, request, context):
        metric = metric_map.get(request.metric)
        top = get_top_posts_by(clickhouse_client, metric)
        return stats_pb2.TopItemsResponse(
            items=[stats_pb2.TopItem(id=r["id"], count=r["count"]) for r in top]
        )

    def GetTopUsersBy(self, request, context):
        metric = metric_map.get(request.metric)
        top = get_top_users_by(clickhouse_client, metric)
        return stats_pb2.TopItemsResponse(
            items=[stats_pb2.TopItem(id=r["id"], count=r["count"]) for r in top]
        )