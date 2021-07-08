from typing import List
from flask import Blueprint, request
from flask_pydantic import validate
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, current_user

from app.models import Note, User, db
from app.schemas import (
    ErrorResponse,
    LoginRequest,
    LoginResponse,
    NoteRequest,
    NoteResponse,
    NotesResponse,
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


notes_router = Blueprint("notes_router", "notes_router")


@notes_router.get("")
@validate()
def notes_get():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    notes = Note.query.paginate(page, per_page)
    notes_response = [NoteResponse(
        id=note.id,
        user_id=note.user_id,
        text=note.text,
        created_at=note.created_at,
        updated_at=note.updated_at
    ) for note in notes.items]

    return NotesResponse(notes=notes_response)


@notes_router.get("<int:id>")
@validate()
def notes_get_single(id: int):
    note = Note.query.filter_by(id=id).one_or_none()
    if note:
        return NoteResponse(
            id=note.id,
            user_id=note.user_id,
            text=note.text,
            created_at=note.created_at,
            updated_at=note.updated_at
        )

    return ErrorResponse(detail="Note not found!"), 404


@notes_router.post("")
@jwt_required()
@validate()
def notes_create(body: NoteRequest):
    note = Note(text=body.text, user_id=current_user.id)
    db.session.add(note)
    db.session.commit()

    return NoteResponse(
        id=note.id,
        user_id=note.user_id,
        text=note.text,
        created_at=note.created_at,
        updated_at=note.updated_at
    )


@notes_router.put("<int:id>")
@jwt_required()
@validate()
def notes_update(id: int, body: NoteRequest):
    note = Note.query.filter_by(id=id).one_or_none()
    if note:
        if note.user_id == current_user.id:
            note.text = body.text
            db.session.commit()
            return NoteResponse(
                id=note.id,
                user_id=note.user_id,
                text=note.text,
                created_at=note.created_at,
                updated_at=note.updated_at
            )
        return ErrorResponse(detail="The note doesn't belong to the user!"), 403

    return ErrorResponse(detail="Note not found!"), 404


@notes_router.delete("<int:id>")
@jwt_required()
@validate()
def notes_delete(id: int):
    note = Note.query.filter_by(id=id).one_or_none()
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return {}
        return ErrorResponse(detail="The note doesn't belong to the user!"), 403

    return ErrorResponse(detail="Note not found!"), 404
