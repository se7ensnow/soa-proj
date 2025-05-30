from sqlalchemy.orm import Session

from post_service_app.post_grpc import post_pb2
from post_service_app.models import Post
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
    return new_post.__dict__

def get_post_by_id(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        return post.__dict__
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
    return post.__dict__

def delete_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return False
    db.delete(post)
    db.commit()
    return True

def list_posts(db: Session, skip: int = 0, limit: int = 100, creator_id: int | None = None):
    query = db.query(Post)
    if creator_id is not None:
        query = query.filter(Post.creator_id == creator_id)
    posts = query.offset(skip).limit(limit).all()
    return [post.__dict__ for post in posts]