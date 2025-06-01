from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    description: str
    is_private: Optional[bool] = False
    tags: Optional[List[str]] = []

class PostUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_private: Optional[bool] = None
    tags: Optional[List[str]] = None

class ListPosts(BaseModel):
    page: int
    size: int
    creator_id: Optional[int] = None

class PostResponse(BaseModel):
    id: int
    title: str
    description: str
    creator_id: int
    created_at: datetime
    updated_at: datetime
    is_private: bool
    tags: List[str]

class PostListResponse(BaseModel):
    posts: List[PostResponse]
    total: int