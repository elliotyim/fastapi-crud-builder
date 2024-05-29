from fastapi import APIRouter

from app.adapter.incoming.web import post, user

router = APIRouter()

router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(post.router, prefix="/posts", tags=["posts"])
