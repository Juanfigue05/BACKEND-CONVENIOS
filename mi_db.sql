DROP DATABASE IF EXISTS mi_proyecto_f;
CREATE DATABASE mi_proyecto_f CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE mi_proyecto_f;

CREATE TABLE rol(
    id_rol SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(20)
);

CREATE TABLE usuario(
    id_usuario INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(80),
    num_documento CHAR(12),
    correo VARCHAR(100) UNIQUE,
    contra_encript VARCHAR(140),
    id_rol SMALLINT UNSIGNED,
    estado BOOLEAN,
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
);

CREATE TABLE municipio (
	id_municipio INT UNSIGNED AUTO_INCREMENT,
	nom_municipio VARCHAR(20),
	PRIMARY KEY(id_municipio)
);

CREATE TABLE instituciones (
	nit_institucion VARCHAR(20),
	nombre_institucion VARCHAR(100),
	direccion VARCHAR(100),
	id_municipio INT UNSIGNED,
	cant_convenios TINYINT,
	PRIMARY KEY(nit_institucion),
	FOREIGN KEY (id_municipio) REFERENCES municipio(id_municipio)
);

CREATE TABLE homologacion (
	id_homologacion INT,
	nit_institucion_destino VARCHAR(20),
	nombre_programa_sena VARCHAR(100),
	cod_programa_sena VARCHAR(50),
	version_programa TINYINT,
	titulo VARCHAR(100),
	programa_ies VARCHAR(50),
	nivel_programa VARCHAR(10),
	snies SMALLINT,
	creditos_homologados TINYINT,
	creditos_totales TINYINT,
	creditos_pendientes TINYINT,
	modalidad VARCHAR(10),
	semestres VARCHAR(5),
	regional VARCHAR(20),
	enlace VARCHAR(100),
	PRIMARY KEY(id_homologacion),
	FOREIGN KEY (nit_institucion_destino) REFERENCES instituciones(nit_institucion)
);

CREATE TABLE egresado_convenio (
	documento VARCHAR(20) NOT NULL UNIQUE,
	num_proceso VARCHAR(20) UNIQUE,
	PRIMARY KEY(documento)
);

CREATE TABLE convenios (
	id_convenio INT AUTO_INCREMENT,
	tipo_convenio VARCHAR(50),
	num_convenio VARCHAR(50),
	nit_institucion VARCHAR(20),
	num_proceso VARCHAR(20),
	nombre_institucion VARCHAR(100),
	estado_convenio VARCHAR(20),
	objetivo_convenio TEXT,
	tipo_proceso VARCHAR(50),
	fecha_firma DATE,
	fecha_inicio DATE,
	duracion_convenio VARCHAR(20),
	plazo_ejecucion DATE,
	prorroga DATE DEFAULT NULL,
	plazo_prorroga DATE,
	duracion_total VARCHAR(20),
	fecha_publicacion_proceso DATE,
	enlace_secop VARCHAR(100),
	supervisor VARCHAR(80),
	precio_estimado DECIMAL(15,2),
	tipo_convenio_sena VARCHAR(50),
	persona_apoyo_fpi VARCHAR(80),	
	enlace_evidencias VARCHAR(100),
	fecha_vigencia DATE,
	PRIMARY KEY(id_convenio),
	FOREIGN KEY(num_proceso) REFERENCES egresado_convenio(num_proceso),
	FOREIGN KEY(nit_institucion) REFERENCES instituciones(nit_institucion)
);

-- CREATE OR REPLACE TABLE grupos (
-- 	ficha VARCHAR(10) UNSIGNED NOT NULL UNIQUE,
-- 	cod_programa INT UNSIGNED,
-- 	cod_centro SMALLINT UNSIGNED,
-- 	modalidad VARCHAR(50),
-- 	jornada VARCHAR(30),
-- 	etapa_ficha VARCHAR(30),
-- 	estado_curso VARCHAR(30),
-- 	fecha_inicio DATE,
-- 	fecha_fin DATE,
-- 	cod_municipio CHAR(5),
-- 	cod_estrategia CHAR(5),
-- 	nombre_responsable VARCHAR(80),
-- 	cupo_asignado SMALLINT UNSIGNED,
-- 	num_aprendices_fem SMALLINT UNSIGNED,
-- 	num_aprendices_mas SMALLINT UNSIGNED,
-- 	num_aprendices_nobin SMALLINT UNSIGNED,
-- 	num_aprendices_matriculados SMALLINT UNSIGNED,
-- 	num_aprendices_activos SMALLINT UNSIGNED,
-- 	tipo_doc_empresa CHAR(3),
-- 	num_doc_empresa VARCHAR(20),
-- 	nombre_empresa VARCHAR(80),
-- 	PRIMARY KEY(ficha),
--     FOREIGN KEY (cod_municipio) REFERENCES municipio(id_municipio),
--     FOREIGN KEY(ficha) REFERENCES egresados(ficha)
-- );

-- CREATE OR REPLACE TABLE egresados (
-- 	documento VARCHAR(15),
-- 	ficha VARCHAR(30) UNIQUE,
-- 	Convenio_media_tecnica BOOLEAN,
-- 	fecha_certificacion DATE,
-- 	estado_certificado VARCHAR(10),
-- 	tipo_documento VARCHAR(15),
-- 	nombre_egresado VARCHAR(30),
-- 	lugar_recidencia VARCHAR(30),
-- 	correo VARCHAR(30),
-- 	tel_principal VARCHAR(15),
-- 	tel_alterno VARCHAR(15),
-- 	PRIMARY KEY(documento),
--     FOREIGN KEY (lugar_recidencia) REFERENCES municipio(id_municipio),
--     FOREIGN KEY(documento) REFERENCES egresado_convenio(documento)
-- );

-- crea un insert de municipios almenos 5 municipios
INSERT INTO municipio (nom_municipio) VALUES
('Bogotá'),
('Medellín'),
('Cali'),
('Barranquilla'),
('Cartagena');


insert into egresado_convenio (documento, num_proceso) values
('1234567890', 'PROC-001'),
('0987654321', 'PROC-002'),
('1122334455', 'PROC-003');
