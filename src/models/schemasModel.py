from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UsuarioSchema(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    correo: EmailStr 
    password: str = Field(..., min_length=6)
    rol: str = Field(..., min_length=5, max_length=10) 
    
    apellido_paterno: Optional[str] = Field(None, min_length=2, max_length=100)
    apellido_materno: Optional[str] = Field(None, min_length=2, max_length=100)
    matricula: Optional[str] = Field(None, min_length=3, max_length=50)
    grado: Optional[str] = Field(None, max_length=10)
    grupo: Optional[str] = Field(None, max_length=10)