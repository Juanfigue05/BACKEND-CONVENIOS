DROP DATABASE IF EXISTS mi_proyecto_f;
CREATE DATABASE mi_proyecto_f CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE mi_proyecto_f;

CREATE TABLE rol (
    id_rol SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(20)
);

CREATE TABLE usuario (
    id_usuario INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(80),
    num_documento CHAR(12),
    correo VARCHAR(100) UNIQUE,
    contra_encript VARCHAR(140),
    id_rol SMALLINT UNSIGNED,
    estado BOOLEAN,
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
);

CREATE TABLE centros_formacion (
    cod_centro SMALLINT UNSIGNED PRIMARY KEY,
    nombre_centro VARCHAR(160),
    cod_regional TINYINT UNSIGNED,
    nombre_regional VARCHAR(80)
);

CREATE TABLE municipio ( 
    id_municipio INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nom_municipio VARCHAR(80),
    codigo_interno VARCHAR(20),
    codigo_dane VARCHAR(20)
);

CREATE TABLE estrategia (
    cod_estrategia CHAR(5) PRIMARY KEY,
    nombre VARCHAR(80)
);

CREATE TABLE programas_formacion (
    cod_programa MEDIUMINT UNSIGNED PRIMARY KEY,
    version CHAR(4),
    nombre VARCHAR(200),
    nivel VARCHAR(70),
    tiempo_duracion SMALLINT UNSIGNED,
    unidad_medida VARCHAR(50),
    estado BOOLEAN,
    url_pdf VARCHAR(180)
);

CREATE TABLE instituciones (
    nit_institucion VARCHAR(20) PRIMARY KEY,
    nombre_institucion VARCHAR(100),
    direccion VARCHAR(100),
    id_municipio INT UNSIGNED,
    cant_convenios TINYINT,
    FOREIGN KEY (id_municipio) REFERENCES municipio(id_municipio)
);

CREATE TABLE homologacion (
    id_homologacion INT PRIMARY KEY,
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
    FOREIGN KEY (nit_institucion_destino) REFERENCES instituciones(nit_institucion)
);

CREATE TABLE egresado_convenio (
    documento VARCHAR(20) PRIMARY KEY,
    num_proceso VARCHAR(20) UNIQUE
);

CREATE TABLE convenios (
    id_convenio INT AUTO_INCREMENT PRIMARY KEY,
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
    prorroga DATE,
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
    FOREIGN KEY (num_proceso) REFERENCES egresado_convenio(num_proceso),
    FOREIGN KEY (nit_institucion) REFERENCES instituciones(nit_institucion)
);

CREATE TABLE grupos (
    ficha VARCHAR(15) PRIMARY KEY,
    cod_programa MEDIUMINT UNSIGNED,
    cod_centro SMALLINT UNSIGNED,
    modalidad VARCHAR(80),
    jornada VARCHAR(80),
    etapa_ficha VARCHAR(80),
    estado_curso VARCHAR(80),
    fecha_inicio DATE,
    fecha_fin DATE,
    id_municipio CHAR(5),
    cod_estrategia CHAR(5),
    nombre_responsable VARCHAR(150),
    cupo_asignado SMALLINT UNSIGNED,
    num_aprendices_fem SMALLINT UNSIGNED,
    num_aprendices_mas SMALLINT UNSIGNED,
    num_aprendices_nobin SMALLINT UNSIGNED,
    num_aprendices_matriculados SMALLINT UNSIGNED,
    num_aprendices_activos SMALLINT UNSIGNED,
    tipo_doc_empresa CHAR(5),
    num_doc_empresa VARCHAR(30),
    nombre_empresa VARCHAR(140),
    FOREIGN KEY (cod_programa) REFERENCES programas_formacion(cod_programa),
    FOREIGN KEY (cod_centro) REFERENCES centros_formacion(cod_centro),
    FOREIGN KEY (id_municipio) REFERENCES municipio(id_municipio),
    FOREIGN KEY (cod_estrategia) REFERENCES estrategia(cod_estrategia)
);

CREATE TABLE egresados (
    documento VARCHAR(20) PRIMARY KEY,
    ficha VARCHAR(15) UNIQUE,
    convenio_media_tecnica BOOLEAN,
    fecha_certificacion DATE,
    estado_certificado VARCHAR(10),
    tipo_documento VARCHAR(15),
    nombre_egresado VARCHAR(100),
    lugar_recidencia CHAR(5),
    correo VARCHAR(100),
    tel_principal VARCHAR(15),
    tel_alterno VARCHAR(15),
    FOREIGN KEY (documento) REFERENCES egresado_convenio(documento),
    FOREIGN KEY (ficha) REFERENCES grupos(ficha),
    FOREIGN KEY (lugar_recidencia) REFERENCES municipio(id_municipio)
);

CREATE TABLE municipio ( 
    id_municipio INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nom_municipio VARCHAR(80),
    codigo_interno VARCHAR(20),
    codigo_dane VARCHAR(20)
);

CREATE TABLE instituciones (
    nit_institucion VARCHAR(20) PRIMARY KEY,
    nombre_institucion VARCHAR(100),
    direccion VARCHAR(100),
    id_municipio INT UNSIGNED,
    cant_convenios TINYINT,
    FOREIGN KEY (id_municipio) REFERENCES municipio(id_municipio)
);

INSERT INTO municipio (nom_municipio,codigo_interno,codigo_dane,codigo_inv) VALUES
('1','Pereira','001','57066001','p-001'),
('Apía','045','660045'),
('Balboa','075','66075'),
('Belen de Umbria','088','66088'),
('Dosquebradas','170','66170'),
('Guática','320','66320'),
('La Celia','383','66383'),
('La Virginia','388','66388'),
('Marsella','430','66430'),
('Mistrató','460','66460'),
('Pueblo Rico','511','66511'),
('Quinchia','533','66535'),
('Santa Rosa de Cabal','685','66685'),
('Santuario','740','66740'),



insert into egresado_convenio (documento, num_proceso) values
('1234567890', 'PROC-001'),
('0987654321', 'PROC-002'),
('1122334455', 'PROC-003');
