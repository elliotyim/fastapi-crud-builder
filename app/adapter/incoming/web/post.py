from fastapi import APIRouter, Depends, Path
from starlette.responses import Response

from app.adapter.incoming.web.schema.request.base import RequestList
from app.adapter.incoming.web.schema.request.post import (
    RequestPostCommentCreate,
    RequestPostCommentUpdate,
    RequestPostCreate,
    RequestPostUpdate,
)
from app.adapter.incoming.web.schema.response.post import (
    ResponsePost,
    ResponsePostComment,
    ResponsePostCommentList,
    ResponsePostList,
)
from app.dependency.crud import crud_service_factory
from app.domain import entity
from app.domain.schema.post import (
    PostCommentCreate,
    PostCommentUpdate,
    PostCreate,
    PostUpdate,
)
from app.domain.service.crud import CRUDService

router = APIRouter()


@router.post("/{post_id}/comments", status_code=201, response_model=ResponsePostComment)
def create_post_comment(
    body: RequestPostCommentCreate,
    post_id: int = Path(..., description="Post ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.PostComment, PostCommentCreate, PostCommentUpdate)
    ),
):
    comment = crud_service.create(PostCommentCreate(post_id=post_id, **body.dict()))
    return ResponsePostComment.model_validate(comment)


@router.get("/{post_id}/comments", response_model=ResponsePostCommentList)
def get_post_comments(
    request_param: RequestList = Depends(RequestList.as_param),
    post_id: int = Path(..., description="Post ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.PostComment, PostCommentCreate, PostCommentUpdate)
    ),
):
    result = crud_service.retrieve_all(
        filter_conditions=[f"post.id::==::{post_id}", *request_param.filter_conditions],
        eager_loading_fields=["author"],
        **request_param.dict(exclude={"filter_conditions"}),
    )
    return ResponsePostCommentList.model_validate(result)


@router.get("/{post_id}/comments/{comment_id}", response_model=ResponsePostComment)
def get_post_comment(
    post_id: int = Path(..., description="Post ID"),
    comment_id: int = Path(..., description="Post Comment ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.PostComment, PostCommentCreate, PostCommentUpdate)
    ),
):
    comment = crud_service.retrieve(pk=comment_id)
    return ResponsePostComment.model_validate(comment)


@router.patch("/{post_id}/comments/{comment_id}", response_model=ResponsePostComment)
def patch_post_comment(
    body: RequestPostCommentUpdate,
    post_id: int = Path(..., description="Post ID"),
    comment_id: int = Path(..., description="Post Comment ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.PostComment, PostCommentCreate, PostCommentUpdate)
    ),
):
    post_comment = crud_service.patch(
        pk=comment_id, update_schema=PostCommentUpdate(**body.dict())
    )
    return ResponsePostComment.model_validate(post_comment)


@router.put("/{post_id}/comments/{comment_id}", response_model=ResponsePostComment)
def put_post_comment(
    body: RequestPostCommentUpdate,
    post_id: int = Path(..., description="Post ID"),
    comment_id: int = Path(..., description="Post Comment ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.PostComment, PostCommentCreate, PostCommentUpdate)
    ),
):
    post_comment = crud_service.put(
        pk=comment_id, update_schema=PostCommentUpdate(**body.dict())
    )
    return ResponsePostComment.model_validate(post_comment)


@router.delete("/{post_id}/comments/{comment_id}", status_code=204, response_model=None)
def delete_post_comment(
    post_id: int = Path(..., description="Post ID"),
    comment_id: int = Path(..., description="Post Comment ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.PostComment, PostCommentCreate, PostCommentUpdate)
    ),
):
    crud_service.delete(pk=comment_id)
    return Response(status_code=204, content=None)


@router.post("", status_code=201, response_model=ResponsePost)
def create_post(
    body: RequestPostCreate,
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.Post, PostCreate, PostUpdate)
    ),
):
    """
    Create a post.
    """
    post = crud_service.create(PostCreate(**body.dict()))
    return ResponsePost.model_validate(post)


@router.get("", response_model=ResponsePostList)
def get_posts(
    request_param: RequestList = Depends(RequestList.as_param),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.Post, PostCreate, PostUpdate)
    ),
):
    """
    Get posts.
    """
    result = crud_service.retrieve_all(
        eager_loading_fields=["author"], **request_param.dict()
    )
    return ResponsePostList.model_validate(result)


@router.get("/{post_id}", response_model=ResponsePost)
def get_post(
    post_id: int = Path(..., description="Post ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.Post, PostCreate, PostUpdate)
    ),
):
    """
    Get a post.
    """
    post = crud_service.retrieve(post_id)
    return ResponsePost.model_validate(post)


@router.patch("/{post_id}", response_model=ResponsePost)
def patch_post(
    body: RequestPostUpdate,
    post_id: int = Path(..., description="Post ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.Post, PostCreate, PostUpdate)
    ),
):
    """
    Update a post partially.\n
    Any null field of body won't be changed.
    """
    post = crud_service.patch(pk=post_id, update_schema=PostUpdate(**body.dict()))
    return ResponsePost.model_validate(post)


@router.put("/{post_id}", response_model=ResponsePost)
def put_post(
    body: RequestPostUpdate,
    post_id: int = Path(..., description="Post ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.Post, PostCreate, PostUpdate)
    ),
):
    """
    Update a post.\n
    If any field of body set null, it will be changed as null.
    """
    post = crud_service.put(pk=post_id, update_schema=PostUpdate(**body.dict()))
    return ResponsePost.model_validate(post)


@router.delete("/{post_id}", status_code=204, response_model=None)
def delete_post(
    post_id: int = Path(..., description="Post ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.Post, PostCreate, PostUpdate)
    ),
):
    """
    Delete a post.
    """
    crud_service.delete(pk=post_id)
    return Response(status_code=204, content=None)
