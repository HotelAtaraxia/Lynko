from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class MateriaSchema(BaseModel):
    id_materia: Optional[int] = None
    nombre: str = Field(..., max_length=50)
    descripcion: Optional[str] = None
    icono: Optional[str] = Field(None, max_length=50)
    link_imagen: Optional[str] = None

    class Config:
        from_attributes = True


class PreguntaSchema(BaseModel):
    id_pregunta: Optional[int] = None
    id_materia: int
    pregunta: str
    nivel_dificultad: int = Field(1, ge=1, le=5)
    puntos_recompensa: int = Field(10, gt=0)

    class Config:
        from_attributes = True


class OpcionSchema(BaseModel):
    id_opcion: Optional[int] = None
    id_pregunta: int
    opcion: str
    es_correcta: bool = False

    class Config:
        from_attributes = True


class ExamenSchema(BaseModel):
    id_examen: Optional[int] = None
    id_materia: int
    titulo: str = Field(..., max_length=150)
    descripcion: Optional[str] = None
    duracion_minutos: int = Field(15, gt=0)
    puntaje_minimo_aprobatorio: int = Field(60, ge=1, le=100)
    fecha_creacion: Optional[datetime] = None

    class Config:
        from_attributes = True


class PreguntaExamenSchema(BaseModel):
    id_examen: int
    id_pregunta: int

    class Config:
        from_attributes = True


class LogroSchema(BaseModel):
    id_logro: Optional[int] = None
    nombre: str = Field(..., max_length=100)
    descripcion: str
    imagen_medalla: Optional[str] = Field(None, max_length=100)

    class Config:
        from_attributes = True

class ExamenConPreguntasResponse(ExamenSchema):
    """Esquema extendido útil para respuestas complejas de administración"""
    preguntas: List[PreguntaSchema] = []
