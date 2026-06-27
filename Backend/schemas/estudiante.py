from pydantic import BaseModel, Field, field_validator
import re

class EstudianteActualizar(BaseModel):
    nombre: str = Field(..., min_length=2, description="El nombre debe tener al menos 2 letras")
    correo: str = Field(..., description="Correo electrónico del estudiante")
    contrasena: str = Field(..., min_length=8, description="La contraseña debe tener mínimo 8 caracteres")

    @field_validator('contrasena')
    @classmethod
    def validar_complejidad_contrasena(cls, v: str) -> str:
        if not re.search(r"[a-zA-Z]", v) or not re.search(r"[0-9]", v):
            raise ValueError("La contraseña debe combinar letras y números.")
        if len(set(v)) < 4:
            raise ValueError("La contraseña debe tener más variedad de caracteres diferentes.")
        return v

    @field_validator('correo')
    @classmethod
    def validar_formato_correo(cls, v: str) -> str:
        if "@" not in v or "." not in v:
            raise ValueError("El correo electrónico no es válido. ¡Revisa el formato!")
        return v
