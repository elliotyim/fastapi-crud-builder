from fastapi import APIRouter, Depends
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


@router.post("")
def create_post(
    body: RequestPostCreate,
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.Post, PostCreate, PostUpdate)
    ),
):
    post = crud_service.create(PostCreate.from_orm(body))
    return JSONResponse(
        status_code=201, content=Post.model_validate(post).model_dump(mode="json")
    )


@router.get("/{id}")
def get_post(
    id: int,
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.Post, PostCreate, PostUpdate)
    ),
):
    post = crud_service.retrieve(id)
    return JSONResponse(content=Post.model_validate(post).model_dump(mode="json"))


@router.patch("/{id}")
def patch_post(
    id: int,
    body: RequestPostUpdate,
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.Post, PostCreate, PostUpdate)
    ),
):
    post = crud_service.patch(pk=id, update_schema=PostUpdate.from_orm(body))
    return JSONResponse(content=Post.model_validate(post).model_dump(mode="json"))


@router.put("/{id}")
def put_post(
    id: int,
    body: RequestPostUpdate,
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.Post, PostCreate, PostUpdate)
    ),
):
    post = crud_service.put(pk=id, update_schema=PostUpdate.from_orm(body))
    return JSONResponse(content=Post.model_validate(post).model_dump(mode="json"))


@router.delete("/{id}")
def delete_post(
    id: int,
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.Post, PostCreate, PostUpdate)
    ),
):
    crud_service.delete(pk=id)
    return JSONResponse(status_code=204, content=None)
