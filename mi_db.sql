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
    id_municipio VARCHAR(20) PRIMARY KEY,
    nom_municipio VARCHAR(80)
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
    id_municipio VARCHAR(20),
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
    id_municipio VARCHAR(20),
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

-- CREATE TABLE egresados (
--     documento VARCHAR(20) PRIMARY KEY,
--     ficha VARCHAR(15) UNIQUE,
--     convenio_media_tecnica BOOLEAN,
--     fecha_certificacion DATE,
--     estado_certificado VARCHAR(10),
--     tipo_documento VARCHAR(15),
--     nombre_egresado VARCHAR(100),
--     lugar_recidencia VARCHAR(20),
--     correo VARCHAR(100),
--     tel_principal VARCHAR(15),
--     tel_alterno VARCHAR(15),
--     FOREIGN KEY (ficha) REFERENCES grupos(ficha),
--     FOREIGN KEY (lugar_recidencia) REFERENCES municipio(id_municipio)
-- );

CREATE TABLE convenios (
    id_convenio INT AUTO_INCREMENT PRIMARY KEY,
    tipo_convenio VARCHAR(50),
    num_convenio VARCHAR(50),
    nit_institucion VARCHAR(20),
    num_proceso VARCHAR(50),
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
    FOREIGN KEY (nit_institucion) REFERENCES instituciones(nit_institucion)
);

-- CREATE TABLE egresado_convenio (
--     id_relacion INT AUTO_INCREMENT PRIMARY KEY,
--     documento VARCHAR(20),
--     id_convenio INT,
--     FOREIGN KEY (documento) REFERENCES egresados(documento),
--     FOREIGN KEY (id_convenio) REFERENCES convenios(id_convenio)
-- );


INSERT INTO municipio (id_municipio,nom_municipio) VALUES
('57066001','Pereira'),
('57066045','Apía'),
('57066075','Balboa'),
('57066088','Belen de Umbria'),
('57066170','Dosquebradas'),
('57066320','Guática'),
('57066383','La Celia'),
('57066388','La Virginia'),
('57066430','Marsella'),
('57066460','Mistrató'),
('57066511','Pueblo Rico'),
('57066535','Quinchia'),
('57066685','Santa Rosa de Cabal'),
('57066740','Santuario');


INSERT INTO instituciones (nit_institucion, nombre_institucion, direccion, id_municipio, cant_convenios) VALUES
('800099310-6', 'ALCALDIA MUNICIPIO DE DOSQUEBRADAS', 'Av. Simón Bolívar No. 36-44 CAM', '57066170', 0),
('891480085-7', 'GOBERNACIÓN DE RISARALDA', 'Calle 19 No. 13-17', '57066001', 0),
('891480030-2', 'MUNICIPIO DE PEREIRA-OFICIAL', 'Cra. 7 No. 18-55', '57066001', 0),
('816005003-5', 'EMPRESA SOCIAL DEL ESTADO SALUD PEREIRA', 'Carrera 7 No. 40-34', '57066001', 0),
('800231235-7', 'E.S.E HOSPITAL UNIVERSITARIO SAN JORGE DE PEREIRA', 'Calle 27 No. 6-40', '57066001', 0),
('800149695', 'FARMASANITAS S.A.S.', 'Carrera 13 No. 26-45', '57066001', 0),
('891409025-4', 'EMPRESA SOCIAL DEL ESTADO HOSPITAL SAN RAFAEL DEL MUNICIPIO DE PUEBLO RICO', 'Calle 6 No. 8-25', '57066511', 0),
('891410661-0', 'EMPRESA SOCIAL DEL ESTADO HOSPITAL SANTA ANA DEL MUNICIPIO DE GUATICA', 'Carrera 5 No. 4-30', '57066320', 0),
('860013798-5', 'UNIVERSIDAD LIBRE DE PEREIRA', 'Belmonte Avenida Las Américas', '57066001', 0),
('891409768-8', 'CORPORACION UNIVERSITARIA SANTA ROSA DE CABAL UNISARC', 'Km 4 Vía Santa Rosa - Chinchiná', '57066685', 0),
('860029924-7', 'UNIVERSIDAD COOPERATIVA DE COLOMBIA - UCC', 'Carrera 7 No. 32-33', '57066001', 0),
('891408248-5', 'CORPORACION INSTITUTO DE ADMINISTRACION Y FINANZAS CIAF', 'Carrera 8 No. 25-67', '57066001', 0),
('891408261-1', 'UNIVERSIDAD CATÓLICA', 'Avenida de las Américas No. 49-95', '57066001', 0),
('900475373', 'INSTITUTO TECNOLOGICO DE DOSQUEBRADAS', 'Carrera 16 No. 32-50', '57066170', 0),
('860020232-8', 'COLEGIO INMACULADO CORAZÓN DE MARIA - RELIGIOSAS FRANCISCANAS', 'Calle 50 No. 14-56', '57066001', 0),
('900077932-5', 'COLEGIO SANTA MARIA GORETTI', 'Carrera 27 No. 75-35', '57066001', 0),
('860010516-1', 'COLEGIO ORDEN DE RELIGIOSAS ADORATRICES DE COLOMBIA', 'Carrera 8 No. 18-35', '57066001', 0),
('890980084-1', 'CONGREGACIÓN SIERVAS DEL SANTISIMO Y DE LA CARIDAD COLEGIO SAN JOSÉ', 'Calle 19 No. 8-41', '57066001', 0),
('900118690-5', 'COLEGIO CONGREGACIÓN RELIGIOSA PROVINCIA DE SAN JOSÉ, HERMANITAS DE LA ANUNCIACIÓN', 'Carrera 9 No. 24-18', '57066001', 0),
('SIN-ID-001', 'COLEGIO SANTA ROSA DE LIMA', 'Carrera 6 No. 12-30', '57066001', 0),
('SIN-ID-002', 'EMPRESA SOCIAL DEL ESTADO HOSPITAL SAN JOSE DEL MUNICIPIO DE BELEN DE UMBRIA', 'Carrera 8 No. 7-45', '57066088', 0),
('800215546-5', 'INSTITUTO NACIONAL PENITENCIARIO Y CARCELARIO INPEC', 'Carrera 54A No. 26A-09', '57066001', 0),
('899999239-2', 'ICBF', 'Avenida Carrera 68 No. 64C-75', '57066001', 0),
('800152783-2', 'FISCALIA', 'Calle 19 No. 7-20', '57066001', 0),
('830131648-6', 'ARN', 'Carrera 9 No. 76-27', '57066001', 0),
('899999022-1', 'MDN', 'Carrera 54 No. 26-25', '57066001', 0);


INSERT INTO rol (nombre_rol) VALUES
('Admin'),
('Instructor'),
('aprendiz');

-- INSERT INTO egresado_convenio (documento, num_proceso) VALUES
-- ('1020304050','PROC-2023-001'),
-- ('1122334455','PROC-2023-002'),
-- ('2233445566','PROC-2023-003');

-- INSERT INTO egresado_convenio (documento, num_proceso) VALUES
-- ('3344556677','PROC-2023-004'),
-- ('4455667788','PROC-2023-005');


DELIMITER //
CREATE TRIGGER tr_convenios_after_insert
AFTER INSERT ON convenios
FOR EACH ROW
BEGIN
    UPDATE instituciones 
    SET cant_convenios = cant_convenios + 1
    WHERE nit_institucion = NEW.nit_institucion;
END//
DELIMITER ;

-- Trigger para DELETE en convenios
DELIMITER //
CREATE TRIGGER tr_convenios_after_delete
AFTER DELETE ON convenios
FOR EACH ROW
BEGIN
    UPDATE instituciones 
    SET cant_convenios = cant_convenios - 1
    WHERE nit_institucion = OLD.nit_institucion;
END//
DELIMITER ;

-- Trigger para UPDATE en convenios (si cambia el NIT)
DELIMITER //
CREATE TRIGGER tr_convenios_after_update
AFTER UPDATE ON convenios
FOR EACH ROW
BEGIN
    IF OLD.nit_institucion <> NEW.nit_institucion THEN
        -- Decrementar en la institución anterior
        UPDATE instituciones 
        SET cant_convenios = cant_convenios - 1
        WHERE nit_institucion = OLD.nit_institucion;
        
        -- Incrementar en la nueva institución
        UPDATE instituciones 
        SET cant_convenios = cant_convenios + 1
        WHERE nit_institucion = NEW.nit_institucion;
    END IF;
END//
DELIMITER ;