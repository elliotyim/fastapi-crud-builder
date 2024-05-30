from fastapi import APIRouter, Depends, Path
from starlette.responses import JSONResponse

from app.adapter.incoming.web.schema.request.post import (
    RequestPostCreate,
    RequestPostUpdate,
)
from app.dependency.crud import crud_service_factory
from app.domain import entity
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


@router.get("/{id}", response_model=Post)
def get_post(
    id: int = Path(..., description="Post ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.Post, PostCreate, PostUpdate)
    ),
):
    """
    Get a post.
    """
    post = crud_service.retrieve(id)
    return JSONResponse(content=Post.model_validate(post).model_dump(mode="json"))


@router.patch("/{id}", response_model=Post)
def patch_post(
    body: RequestPostUpdate,
    id: int = Path(..., description="Post ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.Post, PostCreate, PostUpdate)
    ),
):
    """
    Update a post partially.\n
    Any null field of body won't be changed.
    """
    post = crud_service.patch(pk=id, update_schema=PostUpdate.from_orm(body))
    return JSONResponse(content=Post.model_validate(post).model_dump(mode="json"))


@router.put("/{id}", response_model=Post)
def put_post(
    body: RequestPostUpdate,
    id: int = Path(..., description="Post ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.Post, PostCreate, PostUpdate)
    ),
):
    """
    Update a post.\n
    If any field of body set null, it will be changed as null.
    """
    post = crud_service.put(pk=id, update_schema=PostUpdate.from_orm(body))
    return JSONResponse(content=Post.model_validate(post).model_dump(mode="json"))


@router.delete("/{id}")
def delete_post(
    id: int = Path(..., description="Post ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.Post, PostCreate, PostUpdate)
    ),
):
    """
    Delete a post.
    """
    crud_service.delete(pk=id)
    return JSONResponse(status_code=204, content=None)
