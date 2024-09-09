from fastapi import APIRouter, Depends, Path
from starlette.responses import Response

from app.adapter.incoming.web.schema.request.base import RequestList
from app.adapter.incoming.web.schema.request.user import (
    RequestUserCreate,
    RequestUserUpdate,
)
from app.adapter.incoming.web.schema.response.user import ResponseUser, ResponseUserList
from app.dependency.crud import crud_service_factory
from app.domain import entity
from app.domain.schema.user import UserCreate, UserUpdate
from app.domain.service.crud import CRUDService

router = APIRouter()


@router.post("", status_code=201, response_model=ResponseUser)
def create_user(
    body: RequestUserCreate,
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.User, UserCreate, UserUpdate)
    ),
):
    user = crud_service.create(UserCreate(**body.dict()))
    return ResponseUser.model_validate(user)


@router.get("", response_model=ResponseUserList)
def get_users(
    request_param: RequestList = Depends(RequestList.as_param),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.User, UserCreate, UserUpdate)
    ),
):
    result = crud_service.retrieve_all(**request_param.dict())
    return ResponseUserList.model_validate(result)


@router.get("/{user_id}", response_model=ResponseUser)
def get_user(
    user_id: str = Path(..., description="User ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.User, UserCreate, UserUpdate)
    ),
):
    user = crud_service.retrieve(user_id)
    return ResponseUser.model_validate(user)


@router.patch("/{user_id}", response_model=ResponseUser)
def patch_user(
    body: RequestUserUpdate,
    user_id: str = Path(..., description="User ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.User, UserCreate, UserUpdate)
    ),
):
    user = crud_service.patch(pk=user_id, update_schema=UserUpdate(**body.dict()))
    return ResponseUser.model_validate(user)


@router.put("/{user_id}", response_model=ResponseUser)
def put_user(
    body: RequestUserUpdate,
    user_id: str = Path(..., description="User ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.User, UserCreate, UserUpdate)
    ),
):
    user = crud_service.put(pk=user_id, update_schema=UserUpdate(**body.dict()))
    return ResponseUser.model_validate(user)


@router.delete("/{user_id}", status_code=204, response_model=None)
def delete_user(
    user_id: str = Path(..., description="User ID"),
    crud_service: CRUDService = Depends(
        crud_service_factory(entity.User, UserCreate, UserUpdate)
    ),
):
    crud_service.delete(pk=user_id)
    return Response(status_code=204, content=None)
