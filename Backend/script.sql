DROP TABLE IF EXISTS logros_usuario CASCADE;
DROP TABLE IF EXISTS logros CASCADE;
DROP TABLE IF EXISTS historial_puntos CASCADE;
DROP TABLE IF EXISTS respuestas_usuario CASCADE;
DROP TABLE IF EXISTS intentos_examen CASCADE;
DROP TABLE IF EXISTS preguntas_examen CASCADE;
DROP TABLE IF EXISTS opciones CASCADE;
DROP TABLE IF EXISTS preguntas CASCADE;
DROP TABLE IF EXISTS examenes CASCADE;
DROP TABLE IF EXISTS materias CASCADE;
DROP TABLE IF EXISTS progreso CASCADE;
DROP TABLE IF EXISTS sesiones CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;

CREATE TABLE examenes (
    id_examen integer NOT NULL,
    id_materia integer NOT NULL,
    titulo character varying(150) NOT NULL,
    descripcion text,
    duracion_minutos integer DEFAULT 15,
    puntaje_minimo_aprobatorio integer DEFAULT 60,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT examenes_duracion_minutos_check CHECK ((duracion_minutos > 0)),
    CONSTRAINT examenes_puntaje_minimo_aprobatorio_check CHECK (((puntaje_minimo_aprobatorio >= 1) AND (puntaje_minimo_aprobatorio <= 100)))
);

CREATE SEQUENCE examenes_id_examen_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE examenes_id_examen_seq OWNED BY examenes.id_examen;

CREATE TABLE historial_puntos (
    id_historial integer NOT NULL,
    id_usuario integer NOT NULL,
    puntos_variacion integer NOT NULL,
    motivo character varying(255) NOT NULL,
    fecha_cambio timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

CREATE SEQUENCE historial_puntos_id_historial_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE historial_puntos_id_historial_seq OWNED BY historial_puntos.id_historial;

CREATE TABLE intentos_examen (
    id_intento integer NOT NULL,
    id_usuario integer NOT NULL,
    id_examen integer NOT NULL,
    nota_final integer DEFAULT 0,
    aprobado boolean DEFAULT false,
    fecha_inicio timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_fin timestamp without time zone,
    CONSTRAINT intentos_examen_nota_final_check CHECK (((nota_final >= 0) AND (nota_final <= 100)))
);

CREATE SEQUENCE intentos_examen_id_intento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE intentos_examen_id_intento_seq OWNED BY intentos_examen.id_intento;

CREATE TABLE logros (
    id_logro integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text NOT NULL,
    imagen_medalla character varying(100)
);

CREATE SEQUENCE logros_id_logro_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE logros_id_logro_seq OWNED BY logros.id_logro;

CREATE TABLE logros_usuario (
    id_usuario integer NOT NULL,
    id_logro integer NOT NULL,
    fecha_desbloqueo timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE materias (
    id_materia integer NOT NULL,
    nombre character varying(50) NOT NULL,
    descripcion text,
    icono character varying(50)
);

CREATE SEQUENCE materias_id_materia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE materias_id_materia_seq OWNED BY materias.id_materia;

CREATE TABLE opciones (
    id_opcion integer NOT NULL,
    id_pregunta integer NOT NULL,
    opcion text NOT NULL,
    es_correcta boolean DEFAULT false
);

CREATE SEQUENCE opciones_id_opcion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE opciones_id_opcion_seq OWNED BY opciones.id_opcion;

CREATE TABLE preguntas (
    id_pregunta integer NOT NULL,
    id_materia integer NOT NULL,
    pregunta text NOT NULL,
    nivel_dificultad integer DEFAULT 1,
    puntos_recompensa integer DEFAULT 10,
    CONSTRAINT preguntas_nivel_dificultad_check CHECK (((nivel_dificultad >= 1) AND (nivel_dificultad <= 5))),
    CONSTRAINT preguntas_puntos_recompensa_check CHECK ((puntos_recompensa > 0))
);

CREATE TABLE preguntas_examen (
    id_examen integer NOT NULL,
    id_pregunta integer NOT NULL
);

CREATE SEQUENCE preguntas_id_pregunta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE preguntas_id_pregunta_seq OWNED BY preguntas.id_pregunta;

CREATE TABLE progreso (
    id_progreso integer NOT NULL,
    id_usuario integer,
    id_pregunta integer,
    correcta boolean,
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

CREATE SEQUENCE progreso_id_progreso_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE progreso_id_progreso_seq OWNED BY progreso.id_progreso;

CREATE TABLE respuestas_usuario (
    id_respuesta_user integer NOT NULL,
    id_usuario integer NOT NULL,
    id_intento integer NOT NULL,
    id_pregunta integer NOT NULL,
    id_opcion_seleccionada integer NOT NULL,
    es_correcta boolean NOT NULL
);

CREATE SEQUENCE respuestas_usuario_id_respuesta_user_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE respuestas_usuario_id_respuesta_user_seq OWNED BY respuestas_usuario.id_respuesta_user;

CREATE TABLE sesiones (
    id_sesion integer NOT NULL,
    id_usuario integer NOT NULL,
    token_sesion character varying(255) NOT NULL,
    fecha_creacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion timestamp without time zone NOT NULL
);

CREATE SEQUENCE sesiones_id_sesion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE sesiones_id_sesion_seq OWNED BY sesiones.id_sesion;

CREATE TABLE usuarios (
    id_usuario integer NOT NULL,
    nombre character varying(100) NOT NULL,
    correo character varying(100) NOT NULL,
    "contraseña" character varying(255) NOT NULL,
    puntaje_total integer DEFAULT 0,
    rol character varying(20) DEFAULT 'estudiante'::character varying,
    activo boolean DEFAULT true,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    nivel integer DEFAULT 0,
    dias_racha integer DEFAULT 0,
    CONSTRAINT usuarios_puntaje_total_check CHECK ((puntaje_total >= 0)),
    CONSTRAINT usuarios_rol_check CHECK (((rol)::text = ANY ((ARRAY['estudiante'::character varying, 'admin'::character varying])::text[])))
);

CREATE SEQUENCE usuarios_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE usuarios_id_usuario_seq OWNED BY usuarios.id_usuario;

ALTER TABLE ONLY examenes ALTER COLUMN id_examen SET DEFAULT nextval('examenes_id_examen_seq'::regclass);
ALTER TABLE ONLY historial_puntos ALTER COLUMN id_historial SET DEFAULT nextval('historial_puntos_id_historial_seq'::regclass);
ALTER TABLE ONLY intentos_examen ALTER COLUMN id_intento SET DEFAULT nextval('intentos_examen_id_intento_seq'::regclass);
ALTER TABLE ONLY logros ALTER COLUMN id_logro SET DEFAULT nextval('logros_id_logro_seq'::regclass);
ALTER TABLE ONLY materias ALTER COLUMN id_materia SET DEFAULT nextval('materias_id_materia_seq'::regclass);
ALTER TABLE ONLY opciones ALTER COLUMN id_opcion SET DEFAULT nextval('opciones_id_opcion_seq'::regclass);
ALTER TABLE ONLY preguntas ALTER COLUMN id_pregunta SET DEFAULT nextval('preguntas_id_pregunta_seq'::regclass);
ALTER TABLE ONLY progreso ALTER COLUMN id_progreso SET DEFAULT nextval('progreso_id_progreso_seq'::regclass);
ALTER TABLE ONLY respuestas_usuario ALTER COLUMN id_respuesta_user SET DEFAULT nextval('respuestas_usuario_id_respuesta_user_seq'::regclass);
ALTER TABLE ONLY sesiones ALTER COLUMN id_sesion SET DEFAULT nextval('sesiones_id_sesion_seq'::regclass);
ALTER TABLE ONLY usuarios ALTER COLUMN id_usuario SET DEFAULT nextval('usuarios_id_usuario_seq'::regclass);

ALTER TABLE ONLY examenes ADD CONSTRAINT examenes_pkey PRIMARY KEY (id_examen);
ALTER TABLE ONLY historial_puntos ADD CONSTRAINT historial_puntos_pkey PRIMARY KEY (id_historial);
ALTER TABLE ONLY intentos_examen ADD CONSTRAINT intentos_examen_pkey PRIMARY KEY (id_intento);
ALTER TABLE ONLY logros ADD CONSTRAINT logros_nombre_key UNIQUE (nombre);
ALTER TABLE ONLY logros ADD CONSTRAINT logros_pkey PRIMARY KEY (id_logro);
ALTER TABLE ONLY logros_usuario ADD CONSTRAINT logros_usuario_pkey PRIMARY KEY (id_usuario, id_logro);
ALTER TABLE ONLY materias ADD CONSTRAINT materias_nombre_key UNIQUE (nombre);
ALTER TABLE ONLY materias ADD CONSTRAINT materias_pkey PRIMARY KEY (id_materia);
ALTER TABLE ONLY opciones ADD CONSTRAINT opciones_pkey PRIMARY KEY (id_opcion);
ALTER TABLE ONLY preguntas_examen ADD CONSTRAINT preguntas_examen_pkey PRIMARY KEY (id_examen, id_pregunta);
ALTER TABLE ONLY preguntas ADD CONSTRAINT preguntas_pkey PRIMARY KEY (id_pregunta);
ALTER TABLE ONLY progreso ADD CONSTRAINT progreso_pkey PRIMARY KEY (id_progreso);
ALTER TABLE ONLY respuestas_usuario ADD CONSTRAINT respuestas_usuario_pkey PRIMARY KEY (id_respuesta_user);
ALTER TABLE ONLY sesiones ADD CONSTRAINT sesiones_pkey PRIMARY KEY (id_sesion);
ALTER TABLE ONLY sesiones ADD CONSTRAINT sesiones_token_sesion_key UNIQUE (token_sesion);
ALTER TABLE ONLY usuarios ADD CONSTRAINT usuarios_correo_key UNIQUE (correo);
ALTER TABLE ONLY usuarios ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario);

CREATE INDEX idx_intentos_usuario ON intentos_examen USING btree (id_usuario);
CREATE INDEX idx_puntos_usuario ON historial_puntos USING btree (id_usuario);
CREATE INDEX idx_respuestas_intento ON respuestas_usuario USING btree (id_intento);

ALTER TABLE ONLY examenes ADD CONSTRAINT examenes_id_materia_fkey FOREIGN KEY (id_materia) REFERENCES materias(id_materia) ON DELETE CASCADE;
ALTER TABLE ONLY historial_puntos ADD CONSTRAINT historial_puntos_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE;
ALTER TABLE ONLY intentos_examen ADD CONSTRAINT intentos_examen_id_examen_fkey FOREIGN KEY (id_examen) REFERENCES examenes(id_examen) ON DELETE CASCADE;
ALTER TABLE ONLY intentos_examen ADD CONSTRAINT intentos_examen_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE;
ALTER TABLE ONLY logros_usuario ADD CONSTRAINT logros_usuario_id_logro_fkey FOREIGN KEY (id_logro) REFERENCES logros(id_logro) ON DELETE CASCADE;
ALTER TABLE ONLY logros_usuario ADD CONSTRAINT logros_usuario_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE;
ALTER TABLE ONLY opciones ADD CONSTRAINT opciones_id_pregunta_fkey FOREIGN KEY (id_pregunta) REFERENCES preguntas(id_pregunta) ON DELETE CASCADE;
ALTER TABLE ONLY preguntas_examen ADD CONSTRAINT preguntas_examen_id_examen_fkey FOREIGN KEY (id_examen) REFERENCES examenes(id_examen) ON DELETE CASCADE;
ALTER TABLE ONLY preguntas_examen ADD CONSTRAINT preguntas_examen_id_pregunta_fkey FOREIGN KEY (id_pregunta) REFERENCES preguntas(id_pregunta) ON DELETE CASCADE;
ALTER TABLE ONLY preguntas ADD CONSTRAINT preguntas_id_materia_fkey FOREIGN KEY (id_materia) REFERENCES materias(id_materia) ON DELETE CASCADE;
ALTER TABLE ONLY respuestas_usuario ADD CONSTRAINT respuestas_usuario_id_intento_fkey FOREIGN KEY (id_intento) REFERENCES intentos_examen(id_intento) ON DELETE CASCADE;
ALTER TABLE ONLY respuestas_usuario ADD CONSTRAINT respuestas_usuario_id_opcion_seleccionada_fkey FOREIGN KEY (id_opcion_seleccionada) REFERENCES opciones(id_opcion) ON DELETE CASCADE;
ALTER TABLE ONLY respuestas_usuario ADD CONSTRAINT respuestas_usuario_id_pregunta_fkey FOREIGN KEY (id_pregunta) REFERENCES preguntas(id_pregunta) ON DELETE CASCADE;
ALTER TABLE ONLY respuestas_usuario ADD CONSTRAINT respuestas_usuario_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE;
ALTER TABLE ONLY sesiones ADD CONSTRAINT sesiones_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE;

-- 1. INSERTAR EN LA TABLA: usuarios
INSERT INTO usuarios (id_usuario, nombre, correo, "contraseña", puntaje_total, rol, activo, fecha_registro, nivel, dias_racha) VALUES
(1, 'Administrador Lynko', 'admin@lynko.com', 'Admin1234*', 0, 'admin', true, '2026-06-16 17:35:04.951464', 0, 0),
(3, 'Rodrigo', 'rodrigo@gmail.com', '123456789', 0, 'estudiante', true, '2026-06-19 12:50:08.865713', 0, 0),
(4, 'Freddy Ardila', 'freddycardila@gmail.com', '123456', 0, 'estudiante', true, '2026-06-19 13:25:30.239829', 0, 0),
(5, 'montserrat', 'montsee@gmail.com', 'iori0205', 0, 'estudiante', true, '2026-06-19 14:31:49.29847', 0, 0),
(6, 'Maria Rojas Parra', 'MariaR@gmail.com', '123456789', 0, 'estudiante', true, '2026-06-20 06:44:47.157324', 0, 0),
(7, 'lola la vaca', 'lolita18@hotmail.com', 'Lal0lita18', 0, 'estudiante', true, '2026-06-20 07:09:13.081301', 0, 0),
(8, 'Juan Rulfo', 'juan@rulfo.com', 'Rulfo1234', 0, 'estudiante', true, '2026-06-20 09:45:13.405766', 0, 0);

-- 2. INSERTAR EN LA TABLA: materias
INSERT INTO materias (id_materia, nombre, descripcion, icono) VALUES
(1, 'Matemáticas', 'Aprende a sumar, restar y resolver acertijos numéricos.', 'pi-calculator'),
(2, 'Español', 'Mejora tu lectura, ortografía y descubre grandes historias.', 'book-open'),
(3, 'Biología', 'Explora la naturaleza, los animales y el cuerpo humano.', 'heart-pulse');

-- 3. INSERTAR EN LA TABLA: examenes
INSERT INTO examenes (id_examen, id_materia, titulo, descripcion, duracion_minutos, puntaje_minimo_aprobatorio, fecha_creacion) VALUES
(1, 1, 'Evaluación Inicial de Sumas', 'Demuestra tus habilidades básicas con el Lince de Lynko', 10, 60, '2026-06-16 17:35:04.951464');

-- 4. INSERTAR EN LA TABLA: logros
INSERT INTO logros (id_logro, nombre, descripcion, imagen_medalla) VALUES
(1, 'Primeros Pasos', 'Te has registrado con éxito en Lynko.', 'https://cdn.phototourl.com/free/2026-06-20-e0c8fd52-0006-4bdc-bc45-38a57699562b.png'),
(2, 'Cerebro Matemático', 'Aprobaste tu primer examen de matemáticas con 100%.', 'badge_math.png');

-- 5. INSERTAR EN LA TABLA: logros_usuario
INSERT INTO logros_usuario (id_usuario, id_logro, fecha_desbloqueo) VALUES
(3, 1, '2026-06-19 12:50:08.865713'),
(5, 1, '2026-06-19 14:31:49.29847'),
(6, 1, '2026-06-20 06:44:47.157324'),
(7, 1, '2026-06-20 07:09:13.081301'),
(8, 1, '2026-06-20 09:45:13.405766');

-- 6. INSERTAR EN LA TABLA: preguntas
INSERT INTO preguntas (id_pregunta, id_materia, pregunta, nivel_dificultad, puntos_recompensa) VALUES
(1, 1, '¿Cuánto es 15 + 12?', 1, 10),
(2, 1, 'Si Lynko tiene 5 manzanas y regala 2, ¿cuántas le quedan?', 1, 10),
(3, 2, '¿Cuál de las siguientes palabras es un verbo?', 1, 10),
(4, 3, '¿Qué gas respiramos los seres humanos de manera vital?', 1, 15);

-- 7. INSERTAR EN LA TABLA: preguntas_examen
INSERT INTO preguntas_examen (id_examen, id_pregunta) VALUES
(1, 1),
(1, 2);

-- 8. INSERTAR EN LA TABLA: opciones
INSERT INTO opciones (id_opcion, id_pregunta, opcion, es_correcta) VALUES
(1, 1, '25', false),
(2, 1, '27', true),
(3, 1, '30', false),
(4, 2, '3', true),
(5, 2, '2', false),
(6, 2, '4', false),
(7, 3, 'Perro', false),
(8, 3, 'Cantar', true),
(9, 3, 'Bonito', false),
(10, 4, 'Dióxido de Carbono', false),
(11, 4, 'Oxígeno', true),
(12, 4, 'Nitrógeno', false);

-- 9. AJUSTAR CONTADORES DE LAS SECUENCIAS (Para evitar errores de duplicidad en futuros registros)
SELECT setval('usuarios_id_usuario_seq', 8, true);
SELECT setval('materias_id_materia_seq', 3, true);
SELECT setval('examenes_id_examen_seq', 1, true);
SELECT setval('logros_id_logro_seq', 2, true);
SELECT setval('preguntas_id_pregunta_seq', 4, true);
SELECT setval('opciones_id_opcion_seq', 12, true);
SELECT setval('historial_puntos_id_historial_seq', 1, false);
SELECT setval('intentos_examen_id_intento_seq', 1, false);
SELECT setval('progreso_id_progreso_seq', 1, false);
SELECT setval('respuestas_usuario_id_respuesta_user_seq', 1, false);
SELECT setval('sesiones_id_sesion_seq', 1, false);

ALTER TABLE materias ADD COLUMN link_imagen TEXT;

UPDATE materias 
SET link_imagen = 'https://cdn.phototourl.com/member/2026-06-27-583233bf-4a1d-4970-990f-1d0085dc7d33.png' 
WHERE id_materia = 1;

UPDATE materias 
SET link_imagen = 'https://cdn.phototourl.com/member/2026-06-27-baf14226-a107-4183-9e83-22916f014a7b.png' 
WHERE id_materia = 2;

UPDATE materias 
SET link_imagen = 'https://cdn.phototourl.com/member/2026-06-27-583233bf-4a1d-4970-990f-1d0085dc7d33.png' 
WHERE id_materia = 3;
COMMIT
