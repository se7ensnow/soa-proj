import grpc
from datetime import datetime

from post_service_app.post_grpc import post_pb2_grpc, post_pb2
from post_service_app.database import SessionLocal
from post_service_app.crud import create_post, get_post_by_id, update_post, delete_post, list_posts, add_view, add_comment, add_like, list_comments
from post_service_app.post_kafka.post_producer import send_event

class PostService(post_pb2_grpc.PostServiceServicer):

    def get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def CreatePost(self, request, context):
        db = next(self.get_db())
        post = create_post(db, request)
        return self.post_to_proto(post)

    def GetPostById(self, request, context):
        db = next(self.get_db())
        post = get_post_by_id(db, request.id)
        if post is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")
        return self.post_to_proto(post)

    def UpdatePost(self, request, context):
        db = next(self.get_db())
        post = get_post_by_id(db, request.id)
        if post is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")
        if post.creator_id != request.requestor_id:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "You are not allowed to modify this post")
        post = update_post(db, request)
        return self.post_to_proto(post)

    def DeletePost(self, request, context):
        db = next(self.get_db())
        post = get_post_by_id(db, request.id)
        if post is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")
        if post.creator_id != request.requestor_id:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "You are not allowed to modify this post")
        delete_post(db, request.id)
        return post_pb2.EmptyResponse()

    def ListPosts(self, request, context):
        db = next(self.get_db())
        posts, total = list_posts(db, request.page, request.size, request.creator_id if request.HasField("creator_id") else None)
        post_list = [self.post_to_proto(post) for post in posts]
        return post_pb2.ListPostsResponse(posts=post_list, total=total)

    def ViewPost(self, request, context):
        db = next(self.get_db())
        success = add_view(db, request.post_id, request.user_id)
        if not success:
            context.abort(grpc.StatusCode.INTERNAL, "Failed to add view")
        send_event(
            topic="add_view",
            event_data={
                "post_id": request.post_id,
                "user_id": request.user_id,
                "timestamp": datetime.now().isoformat(),
            }
        )
        return post_pb2.EmptyResponse()

    def LikePost(self, request, context):
        db = next(self.get_db())
        success = add_like(db, request.post_id, request.user_id)
        if not success:
            context.abort(grpc.StatusCode.INTERNAL, "Failed to add like")
        send_event(
            topic="add_like",
            event_data={
                "post_id": request.post_id,
                "user_id": request.user_id,
                "timestamp": datetime.now().isoformat(),
            }
        )
        return post_pb2.EmptyResponse()

    def AddComment(self, request, context):
        db = next(self.get_db())
        comment = add_comment(db, request.post_id, request.user_id, request.content)
        send_event(
            topic="add_comment",
            event_data={
                "post_id": request.post_id,
                "user_id": request.user_id,
                "timestamp": datetime.now().isoformat(),
            }
        )
        return post_pb2.CommentResponse(
            id = comment.id,
            post_id = comment.post_id,
            user_id = comment.user_id,
            content = comment.content,
            created_at = comment.created_at.isoformat()
        )

    def ListComments(self, request, context):
        db = next(self.get_db())
        comments, total = list_comments(db, request.post_id, request.page, request.size)
        comment_list = [
            post_pb2.CommentResponse(
                id=c.id,
                post_id=c.post_id,
                user_id=c.user_id,
                content=c.content,
                created_at=c.created_at.isoformat()
            )
            for c in comments
        ]
        return post_pb2.ListCommentsResponse(comments=comment_list, total=total)

    def post_to_proto(self, post):
        return post_pb2.PostResponse(
            id = post.id,
            title = post.title,
            description = post.description,
            creator_id = post.creator_id,
            created_at = post.created_at.isoformat(),
            updated_at = post.updated_at.isoformat(),
            is_private = post.is_private,
            tags = post.tags,
            likes_count = post.likes_count,
            views_count = post.views_count
        )