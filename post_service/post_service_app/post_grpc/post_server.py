import grpc
from post_service_app.post_grpc import post_pb2_grpc, post_pb2
from post_service_app.database import SessionLocal
from post_service_app.crud import create_post, get_post_by_id, update_post, delete_post, list_posts

class PostService(post_pb2_grpc.PostServiceServicer):
    def __init__(self):
        self.db_session = SessionLocal

    def CreatePost(self, request, context):
        with self.db_session() as db:
            post = create_post(db, request)
            post_response = post_pb2.PostResponse(
                id=post['id'],
                title=post['title'],
                description=post['description'],
                creator_id=post['creator_id'],
                created_at=post['created_at'].isoformat(),
                updated_at=post['updated_at'].isoformat(),
                is_private=post['is_private'],
                tags=post['tags'],
            )
            return post_response

    def GetPostById(self, request, context):
        with self.db_session() as db:
            post = get_post_by_id(db, request.id)
            if post is None:
                context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")
            post_response = post_pb2.PostResponse(
                id=post['id'],
                title=post['title'],
                description=post['description'],
                creator_id=post['creator_id'],
                created_at=post['created_at'].isoformat(),
                updated_at=post['updated_at'].isoformat(),
                is_private=post['is_private'],
                tags=post['tags'],
            )
            return post_response

    def UpdatePost(self, request, context):
        with self.db_session() as db:
            post = get_post_by_id(db, request.id)
            if post is None:
                context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")
            if post['creator_id'] != request.requestor_id:
                context.abort(grpc.StatusCode.PERMISSION_DENIED, "You are not allowed to modify this post")
            post = update_post(db, request)
            post_response = post_pb2.PostResponse(
                id=post['id'],
                title=post['title'],
                description=post['description'],
                creator_id=post['creator_id'],
                created_at=post['created_at'].isoformat(),
                updated_at=post['updated_at'].isoformat(),
                is_private=post['is_private'],
                tags=post['tags'],
            )
            return post_response

    def DeletePost(self, request, context):
        with self.db_session() as db:
            post = get_post_by_id(db, request.id)
            if post is None:
                context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")
            if post['creator_id'] != request.requestor_id:
                context.abort(grpc.StatusCode.PERMISSION_DENIED, "You are not allowed to modify this post")
            delete_post(db, request.id)
            return post_pb2.EmptyResponse()

    def ListPosts(self, request, context):
        with self.db_session() as db:
            posts = list_posts(db, request.skip, request.limit, request.creator_id)
            for post in posts:
                post_response = post_pb2.PostResponse(
                    id=post['id'],
                    title=post['title'],
                    description=post['description'],
                    creator_id=post['creator_id'],
                    created_at=post['created_at'].isoformat(),
                    updated_at=post['updated_at'].isoformat(),
                    is_private=post['is_private'],
                    tags=post['tags'],
                )
                yield post_response