from fastapi import APIRouter, Depends, Path
from starlette.responses import Response

from app.adapter.incoming.web.schema.request.base import RequestList
from app.adapter.incoming.web.schema.request.post import (
    RequestPostCreate,
    RequestPostUpdate,
)
from app.adapter.incoming.web.schema.response.post import ResponsePost, ResponsePostList
from app.dependency.crud import crud_service_factory
from app.domain import entity
from app.domain.schema.post import PostCreate, PostUpdate
from app.domain.service.crud import CRUDService

router = APIRouter()


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
    post = crud_service.create(PostCreate.from_orm(body))
    return ResponsePost.model_validate(post)


@router.get("", status_code=200, response_model=ResponsePostList)
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


@router.get("/{post_id}", status_code=200, response_model=ResponsePost)
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


@router.patch("/{post_id}", status_code=200, response_model=ResponsePost)
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
    post = crud_service.patch(pk=post_id, update_schema=PostUpdate.from_orm(body))
    return ResponsePost.model_validate(post)


@router.put("/{post_id}", status_code=200, response_model=ResponsePost)
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
    post = crud_service.put(pk=post_id, update_schema=PostUpdate.from_orm(body))
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
