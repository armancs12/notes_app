from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr, validator


class ErrorResponse(BaseModel):
    detail: str


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

    @validator('name')
    def name_must_be_full_name(cls, name):
        if ' ' not in name:
            raise ValueError('must be full name')
        return name.title()

    @validator('password')
    def password_must_be_secure(cls, password):
        if not password.isalnum():
            raise ValueError('must be alpha-numeric')
        if len(password) < 8:
            raise ValueError('must be at least 8 characters')
        return password


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class ProfileResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr


class RefreshTokenResponse(BaseModel):
    access_token: str


class NoteRequest(BaseModel):
    text: str


class NoteResponse(BaseModel):
    id: str
    user_id: str
    text: str
    created_at: datetime
    updated_at: datetime


class NotesResponse(BaseModel):
    notes: List[NoteResponse]
