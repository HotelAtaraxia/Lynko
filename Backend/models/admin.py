import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Materia(Base):
    __tablename__ = 'materias'
    
    id_materia = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String, nullable=True)
    icono = Column(String(50), nullable=True)
    link_imagen = Column(String, nullable=True)


class Pregunta(Base):
    __tablename__ = 'preguntas'
    
    id_pregunta = Column(Integer, primary_key=True, autoincrement=True)
    id_materia = Column(Integer, ForeignKey('materias.id_materia', ondelete='CASCADE'), nullable=False)
    pregunta = Column(String, nullable=False)
    nivel_dificultad = Column(Integer, default=1)
    puntos_recompensa = Column(Integer, default=10)

    __table_args__ = (
        CheckConstraint('nivel_dificultad >= 1 AND nivel_dificultad <= 5', name='preguntas_nivel_dificultad_check'),
        CheckConstraint('puntos_recompensa > 0', name='preguntas_puntos_recompensa_check'),
    )


class Opcion(Base):
    __tablename__ = 'opciones'
    
    id_opcion = Column(Integer, primary_key=True, autoincrement=True)
    id_pregunta = Column(Integer, ForeignKey('preguntas.id_pregunta', ondelete='CASCADE'), nullable=False)
    opcion = Column(String, nullable=False)
    es_correcta = Column(Boolean, default=False)


class Examen(Base):
    __tablename__ = 'examenes'
    
    id_examen = Column(Integer, primary_key=True, autoincrement=True)
    id_materia = Column(Integer, ForeignKey('materias.id_materia', ondelete='CASCADE'), nullable=False)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(String, nullable=True)
    duracion_minutos = Column(Integer, default=15)
    puntaje_minimo_aprobatorio = Column(Integer, default=60)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        CheckConstraint('duracion_minutos > 0', name='examenes_duracion_minutos_check'),
        CheckConstraint('puntaje_minimo_aprobatorio >= 1 AND puntaje_minimo_aprobatorio <= 100', name='examenes_puntaje_minimo_aprobatorio_check'),
    )


class PreguntaExamen(Base):
    __tablename__ = 'preguntas_examen'
    
    id_examen = Column(Integer, ForeignKey('examenes.id_examen', ondelete='CASCADE'), primary_key=True)
    id_pregunta = Column(Integer, ForeignKey('preguntas.id_pregunta', ondelete='CASCADE'), primary_key=True)


class Logro(Base):
    __tablename__ = 'logros'
    
    id_logro = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String, nullable=False)
    imagen_medalla = Column(String(100), nullable=True)
