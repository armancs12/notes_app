from flask import Blueprint
from flask_pydantic import validate
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, current_user

from app.models import User, db
from app.schemas import (
    ErrorResponse,
    LoginRequest,
    LoginResponse,
    ProfileResponse,
    RefreshTokenResponse,
    RegisterRequest
)

auth_router = Blueprint("auth_router", "auth_router")


@auth_router.post('/register')
@validate()
def auth_register(body: RegisterRequest):
    user_exist = User.query.filter_by(email=body.email).one_or_none()
    if user_exist:
        return ErrorResponse(detail="User with the email is already exist!")

    user = User(body.name, body.email, body.password)
    db.session.add(user)
    db.session.commit()

    return ProfileResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email
    ), 201


@auth_router.post('/login')
@validate()
def auth_login(body: LoginRequest):
    user: User = User.query.filter_by(email=body.email).one_or_none()
    if user and user.check_password(body.password):

        access = create_access_token(identity=user)
        refresh = create_refresh_token(identity=user)
        return LoginResponse(access_token=access, refresh_token=refresh)

    return ErrorResponse(detail="Username or password is not correct!")


@auth_router.post('/refresh_token')
@validate()
@jwt_required(refresh=True)
def auth_refresh_token():
    access = create_access_token(identity=current_user)
    return RefreshTokenResponse(access_token=access)


@auth_router.get('/profile')
@jwt_required()
@validate()
def auth_profile():
    return ProfileResponse(
        id=current_user.id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
    )
