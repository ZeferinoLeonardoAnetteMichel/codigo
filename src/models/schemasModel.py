from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UsuarioSchema(BaseModel):
    nombre: str = Field(min_length=3, max_length=100)
    apellido:str=Field(min_length=3,max_length=100)
    correo: EmailStr
    password: str = Field(min_length=6)
    
