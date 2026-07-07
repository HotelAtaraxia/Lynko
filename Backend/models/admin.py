from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UsuarioModel(BaseModel):
    id_usuario: int
    nombre: str = Field(..., max_length=100)
    correo: EmailStr
    contrasena: str = Field(..., alias="contraseña")
    puntaje_total: int = 0
    rol: str = "estudiante"
    activo: bool = True
    fecha_registro: datetime = Field(default_factory=datetime.now)
    nivel: int = 0
    dias_racha: int = 0

    class Config:
        populate_by_name = True

class MateriaModel(BaseModel):
    id_materia: int
    nombre: str = Field(..., max_length=50)
    descripcion: Optional[str] = None
    icono: Optional[str] = Field(None, max_length=50)
    link_imagen: Optional[str] = None

class PreguntaModel(BaseModel):
    id_pregunta: int
    id_materia: int
    pregunta: str
    nivel_dificultad: int = Field(1, ge=1, le=5)
    puntos_recompensa: int = Field(10, gt=0)

class OpcionModel(BaseModel):
    id_opcion: int
    id_pregunta: int
    opcion: str
    es_correcta: bool

class ExamenModel(BaseModel):
    id_examen: int
    id_materia: int
    titulo: str = Field(..., max_length=150)
    descripcion: Optional[str] = None
    duracion_minutos: int = Field(15, gt=0)
    puntaje_minimo_aprobatorio: int = Field(60, ge=1, le=100)
    fecha_creacion: datetime = Field(default_factory=datetime.now)

class IntentoExamenModel(BaseModel):
    id_intento: int
    id_usuario: int
    id_examen: int
    nota_final: int = Field(0, ge=0, le=100)
    aprobado: bool = False
    fecha_inicio: datetime = Field(default_factory=datetime.now)
    fecha_fin: Optional[datetime] = None

class RespuestaUsuarioModel(BaseModel):
    id_respuesta_user: int
    id_usuario: int
    id_intento: int
    id_pregunta: int
    id_opcion_seleccionada: int
    es_correcta: bool

class ProgresoModel(BaseModel):
    id_progreso: int
    id_usuario: int
    id_pregunta: int
    correcta: bool
    fecha: datetime = Field(default_factory=datetime.now)

class LogroModel(BaseModel):
    id_logro: int
    nombre: str = Field(..., max_length=100)
    descripcion: str
    imagen_medalla: Optional[str] = Field(None, max_length=100)

class LogroUsuarioModel(BaseModel):
    id_usuario: int
    id_logro: int
    fecha_desbloqueo: datetime = Field(default_factory=datetime.now)

class HistorialPuntosModel(BaseModel):
    id_historial: int
    id_usuario: int
    puntos_variacion: int
    motivo: str = Field(..., max_length=255)
    fecha_cambio: datetime = Field(default_factory=datetime.now)

class SesionModel(BaseModel):
    id_sesion: int
    id_usuario: int
    token_sesion: str = Field(..., max_length=255)
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    fecha_expiracion: datetime
