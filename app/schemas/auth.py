
from pydantic import BaseModel, EmailStr, Field


class CadastroRequest(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=8, max_length=72)


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
