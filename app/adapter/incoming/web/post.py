from fastapi import APIRouter, Depends, Path
from starlette.responses import JSONResponse

from app.adapter.incoming.web.schema.request.base import RequestList
from app.adapter.incoming.web.schema.request.post import (
    RequestPostCreate,
    RequestPostUpdate,
)
from app.dependency.crud import crud_service_factory
from app.domain import entity
from app.domain.schema.base import PaginatedList
from app.domain.schema.post import Post, PostCreate, PostUpdate
from app.domain.service.crud import CRUDService

router = APIRouter()


@router.post("", response_model=Post)
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
    return JSONResponse(
        status_code=201, content=Post.model_validate(post).model_dump(mode="json")
    )


@router.get("", response_model=PaginatedList)
def get_posts(
    request_param: RequestList = Depends(RequestList.as_param),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.Post, PostCreate, PostUpdate)
    ),
):
    result = crud_service.retrieve_all(
        eager_loading_fields=["author"], **request_param.dict()
    )
    return result


@router.get("/{post_id}", response_model=Post)
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
    return JSONResponse(content=Post.model_validate(post).model_dump(mode="json"))


@router.patch("/{post_id}", response_model=Post)
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
    return JSONResponse(content=Post.model_validate(post).model_dump(mode="json"))


@router.put("/{post_id}", response_model=Post)
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
    return JSONResponse(content=Post.model_validate(post).model_dump(mode="json"))


@router.delete("/{post_id}")
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
    return JSONResponse(status_code=204, content=None)
