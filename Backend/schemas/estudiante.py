from typing import List
from pydantic import BaseModel

class DatosBaseEstudianteResponse(BaseModel):
    """Estructura que retorna 'obtener_datos_base_estudiante()'"""
    nombre: str
    puntos: int
    nivel: int
    racha: int
    correo: str
    contrasena: str
    contraseña: str 

class OpcionLandingSchema(BaseModel):
    """Sub-estructura para las opciones de la landing"""
    opcion: str
    es_correcta: bool

class PreguntaLandingResponse(BaseModel):
    """Estructura compleja que retorna 'consultar_preguntas_landing()'"""
    id_pregunta: int
    materia: str  
    pregunta: str
    puntos: int
    opciones: List[OpcionLandingSchema]

class DashboardEstudianteResponse(BaseModel):
    """Estructura que retorna 'consultar_dashboard_estudiante()'"""
    nombre: str
    puntaje_total: int
    nivel: int
    dias_racha: int
