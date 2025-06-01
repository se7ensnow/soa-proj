from sqlalchemy.orm import Session

from post_service_app.post_grpc import post_pb2
from post_service_app.models import Post, Comment
from datetime import datetime

def create_post(db: Session, request):
    new_post = Post(
        title=request.title,
        description=request.description,
        creator_id=request.creator_id,
        is_private=request.is_private,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        tags=request.tags
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_post_by_id(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        return post
    return None

def update_post(db: Session, request):
    post = db.query(Post).filter(Post.id == request.id).first()
    if not post:
        return None
    post.title = request.title
    post.description = request.description
    post.is_private = request.is_private
    post.updated_at = datetime.now()
    post.tags = request.tags
    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return False
    db.delete(post)
    db.commit()
    return True

def list_posts(db: Session, page: int = 0, size: int = 100, creator_id: int | None = None):
    query = db.query(Post)
    if creator_id is not None:
        query = query.filter(Post.creator_id == creator_id)
    total = query.count()
    posts = query.order_by(Post.updated_at.desc()).offset((page - 1) * size).limit(size).all()
    return posts, total

def add_view(db: Session, post_id: int, user_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return False
    post.views_count += 1
    db.commit()
    return True

def add_like(db: Session, post_id: int, user_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return False
    post.likes_count += 1
    db.commit()
    return True

def add_comment(db: Session, post_id: int, user_id: int, content: str):
    comment = Comment(
        post_id=post_id,
        user_id=user_id,
        content=content,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def list_comments(db: Session, post_id: int, page: int, size: int):
    query = db.query(Comment).filter(Comment.post_id == post_id)
    total = query.count()
    comments = query.order_by(Comment.created_at.desc()).offset((page - 1) * size).limit(size).all()
    return comments, total