-- Eliminar base de datos si existe y crearla
DROP DATABASE IF EXISTS railway;
CREATE DATABASE railway CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE railway;

-- ============================================================
-- SECCIÓN 1: CREACIÓN DE TABLAS
-- ============================================================

-- ------------------------------------------------------------
-- Tabla: rol
-- Descripción: Roles de usuario del sistema
-- ------------------------------------------------------------
CREATE TABLE rol (
    id_rol SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(20) NOT NULL,
    INDEX idx_nombre_rol (nombre_rol)
) ENGINE=InnoDB COMMENT='Roles de usuario del sistema';

-- ------------------------------------------------------------
-- Tabla: usuario
-- Descripción: Usuarios del sistema
-- ------------------------------------------------------------
CREATE TABLE usuario (
    id_usuario INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(80) NOT NULL,
    num_documento CHAR(12) NOT NULL UNIQUE,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contra_encript VARCHAR(140) NOT NULL,
    id_rol SMALLINT UNSIGNED NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_correo (correo),
    INDEX idx_estado (estado),
    INDEX idx_rol (id_rol)
) ENGINE=InnoDB COMMENT='Usuarios del sistema';

-- ------------------------------------------------------------
-- Tabla: municipio
-- Descripción: Municipios del departamento de Risaralda
-- ------------------------------------------------------------
CREATE TABLE municipio ( 
    id_municipio VARCHAR(20) PRIMARY KEY,
    nom_municipio VARCHAR(80) NOT NULL,
    INDEX idx_nombre_municipio (nom_municipio)
) ENGINE=InnoDB COMMENT='Municipios de Risaralda';

-- ------------------------------------------------------------
-- Tabla: instituciones
-- Descripción: Instituciones con convenios
-- ------------------------------------------------------------
CREATE TABLE instituciones (
    nit_institucion VARCHAR(20) PRIMARY KEY,
    nombre_institucion VARCHAR(100) NOT NULL,
    direccion VARCHAR(100),
    id_municipio VARCHAR(20) NOT NULL,
    cant_convenios TINYINT UNSIGNED DEFAULT 0,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_municipio) REFERENCES municipio(id_municipio) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_nombre_institucion (nombre_institucion),
    INDEX idx_municipio (id_municipio),
    INDEX idx_cant_convenios (cant_convenios)
) ENGINE=InnoDB COMMENT='Instituciones con convenios';

-- ------------------------------------------------------------
-- Tabla: convenios
-- Descripción: Convenios interinstitucionales
-- ------------------------------------------------------------
CREATE TABLE convenios (
    id_convenio INT AUTO_INCREMENT PRIMARY KEY,
    tipo_convenio VARCHAR(50),
    num_convenio VARCHAR(50) NOT NULL,
    nit_institucion VARCHAR(20) NOT NULL,
    num_proceso VARCHAR(50) DEFAULT NULL,
    nombre_institucion VARCHAR(120),
    estado_convenio VARCHAR(50),
    objetivo_convenio VARCHAR(1000) DEFAULT NULL,
    tipo_proceso VARCHAR(50),
    fecha_firma VARCHAR(50),   
    fecha_inicio VARCHAR(50),   
    duracion_convenio VARCHAR(20),
    plazo_ejecucion VARCHAR(50),   
    prorroga VARCHAR(50),   
    plazo_prorroga VARCHAR(50),   
    duracion_total VARCHAR(20),
    fecha_publicacion_proceso VARCHAR(50),   
    enlace_secop VARCHAR(1500),
    supervisor VARCHAR(400),
    precio_estimado DECIMAL(15,2),
    tipo_convenio_sena VARCHAR(50),
    persona_apoyo_fpi VARCHAR(80),
    enlace_evidencias TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (nit_institucion) REFERENCES instituciones(nit_institucion) ON DELETE RESTRICT ON UPDATE CASCADE,
    UNIQUE KEY uk_convenio_unico (num_convenio, nit_institucion),
    INDEX idx_estado_convenio (estado_convenio),
    INDEX idx_tipo_convenio_sena (tipo_convenio_sena),
    INDEX idx_persona_apoyo (persona_apoyo_fpi),
    INDEX idx_fecha_firma (fecha_firma),
    INDEX idx_nit_institucion (nit_institucion)
) ENGINE=InnoDB COMMENT='Convenios interinstitucionales';

-- ------------------------------------------------------------
-- Tabla: homologacion
-- Descripción: Homologaciones de programas académicos
-- ------------------------------------------------------------
CREATE TABLE homologacion (
    id_homologacion INT AUTO_INCREMENT PRIMARY KEY,
    nit_institucion_destino VARCHAR(30) NOT NULL,
    nombre_programa_sena VARCHAR(200),
    cod_programa_sena VARCHAR(50),
    version_programa TINYINT,
    titulo VARCHAR(150),
    programa_ies VARCHAR(80),
    nivel_programa VARCHAR(50),
    snies INT,
    creditos_homologados INT,
    creditos_totales INT,
    creditos_pendientes INT,
    modalidad VARCHAR(20),
    semestres VARCHAR(5),
    regional VARCHAR(30),
    enlace VARCHAR(255),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (nit_institucion_destino) REFERENCES instituciones(nit_institucion) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_modalidad (modalidad),
    INDEX idx_nivel_programa (nivel_programa),
    INDEX idx_regional (regional),
    INDEX idx_programa_ies (programa_ies),
    INDEX idx_nit_institucion (nit_institucion_destino)
) ENGINE=InnoDB COMMENT='Homologaciones de programas académicos';

-- ------------------------------------------------------------
-- Tabla: estadistica_categoria
-- Descripción: Tabla unificada para todas las estadísticas del sistema
-- ------------------------------------------------------------
CREATE TABLE estadistica_categoria (
    id_estadistica INT AUTO_INCREMENT PRIMARY KEY,
    categoria VARCHAR(50) NOT NULL COMMENT 'Categoría de la estadística',
    nombre VARCHAR(400) NOT NULL COMMENT 'Nombre del elemento estadístico',
    subcategoria VARCHAR(50) DEFAULT NULL COMMENT 'Subcategoría opcional para filtros adicionales',
    cantidad INT DEFAULT 0 COMMENT 'Contador principal de registros',
    suma_total DECIMAL(15,2) DEFAULT 0 COMMENT 'Suma acumulada de montos o valores numéricos',
    metadata JSON DEFAULT NULL COMMENT 'Información adicional flexible en formato JSON',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_categoria_nombre (categoria, nombre),
    INDEX idx_categoria (categoria, nombre),
    INDEX idx_fecha (fecha_actualizacion),
    INDEX idx_cantidad (cantidad DESC)
) ENGINE=InnoDB COMMENT='Estadísticas unificadas del sistema';


-- ============================================================
-- SECCIÓN 2: TRIGGERS
-- ============================================================

DELIMITER $$

-- ------------------------------------------------------------
-- TRIGGERS PARA TABLA: instituciones
-- Descripción: Actualizar cant_convenios automáticamente
-- ------------------------------------------------------------

-- Trigger: Actualizar cant_convenios después de INSERT en convenios
DROP TRIGGER IF EXISTS tr_convenios_after_insert$$
CREATE TRIGGER tr_convenios_after_insert
AFTER INSERT ON convenios
FOR EACH ROW
BEGIN
    UPDATE instituciones
    SET cant_convenios = (
        SELECT COUNT(*) 
        FROM convenios 
        WHERE nit_institucion = NEW.nit_institucion
    )
    WHERE nit_institucion = NEW.nit_institucion;
END$$

-- Trigger: Actualizar cant_convenios después de DELETE en convenios
DROP TRIGGER IF EXISTS tr_convenios_after_delete$$
CREATE TRIGGER tr_convenios_after_delete
AFTER DELETE ON convenios
FOR EACH ROW
BEGIN
    UPDATE instituciones 
    SET cant_convenios = (
        SELECT COUNT(*) 
        FROM convenios 
        WHERE nit_institucion = OLD.nit_institucion
    )
    WHERE nit_institucion = OLD.nit_institucion;
END$$

-- Trigger: Actualizar cant_convenios después de UPDATE en convenios
DROP TRIGGER IF EXISTS tr_convenios_after_update_instituciones$$
CREATE TRIGGER tr_convenios_after_update_instituciones
AFTER UPDATE ON convenios
FOR EACH ROW
BEGIN
    -- Si cambió el NIT de la institución
    IF OLD.nit_institucion <> NEW.nit_institucion THEN
        -- Recalcular la institución anterior
        UPDATE instituciones 
        SET cant_convenios = (
            SELECT COUNT(*) 
            FROM convenios 
            WHERE nit_institucion = OLD.nit_institucion
        )
        WHERE nit_institucion = OLD.nit_institucion;
        
        -- Recalcular la nueva institución
        UPDATE instituciones 
        SET cant_convenios = (
            SELECT COUNT(*) 
            FROM convenios 
            WHERE nit_institucion = NEW.nit_institucion
        )
        WHERE nit_institucion = NEW.nit_institucion;
    END IF;
END$$

-- ------------------------------------------------------------
-- TRIGGERS PARA TABLA: convenios - Estadísticas
-- Descripción: Actualizar estadísticas automáticamente
-- ------------------------------------------------------------

-- Trigger: INSERT - Actualizar estadísticas al insertar convenio
DROP TRIGGER IF EXISTS tr_convenios_insert_estadisticas$$
CREATE TRIGGER tr_convenios_insert_estadisticas
AFTER INSERT ON convenios
FOR EACH ROW
BEGIN
    -- 1. Estadística: tipo_convenio_sena
    IF NEW.tipo_convenio_sena IS NOT NULL THEN
        INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
        VALUES ('tipo_convenio', NEW.tipo_convenio_sena, 1)
        ON DUPLICATE KEY UPDATE 
            cantidad = cantidad + 1,
            fecha_actualizacion = CURRENT_TIMESTAMP;
    END IF;
    
    -- 2. Estadística: persona_apoyo_fpi
    IF NEW.persona_apoyo_fpi IS NOT NULL THEN
        INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
        VALUES ('persona_apoyo_fpi', NEW.persona_apoyo_fpi, 1)
        ON DUPLICATE KEY UPDATE 
            cantidad = cantidad + 1,
            fecha_actualizacion = CURRENT_TIMESTAMP;
    END IF;
    
    -- 3. Estadística: estado_convenio
    IF NEW.estado_convenio IS NOT NULL THEN
        INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
        VALUES ('estado_convenio', NEW.estado_convenio, 1)
        ON DUPLICATE KEY UPDATE 
            cantidad = cantidad + 1,
            fecha_actualizacion = CURRENT_TIMESTAMP;
    END IF;
    
    -- 4. Estadística: tipo_proceso
    IF NEW.tipo_proceso IS NOT NULL THEN
        INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
        VALUES ('tipo_proceso', NEW.tipo_proceso, 1)
        ON DUPLICATE KEY UPDATE 
            cantidad = cantidad + 1,
            fecha_actualizacion = CURRENT_TIMESTAMP;
    END IF;
    
    -- 5. Estadística: supervisor (carga de trabajo)
    IF NEW.supervisor IS NOT NULL THEN
        INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
        VALUES ('supervisor', NEW.supervisor, 1)
        ON DUPLICATE KEY UPDATE 
            cantidad = cantidad + 1,
            fecha_actualizacion = CURRENT_TIMESTAMP;
    END IF;
    
    -- 6. Estadística: tipo_convenio general
    IF NEW.tipo_convenio IS NOT NULL THEN
        INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
        VALUES ('tipo_convenio_general', NEW.tipo_convenio, 1)
        ON DUPLICATE KEY UPDATE 
            cantidad = cantidad + 1,
            fecha_actualizacion = CURRENT_TIMESTAMP;
    END IF;
    
    -- 7. Estadística: Sumar precio_estimado por tipo_convenio_sena
    IF NEW.precio_estimado IS NOT NULL AND NEW.tipo_convenio_sena IS NOT NULL THEN
        INSERT INTO estadistica_categoria (categoria, nombre, cantidad, suma_total)
        VALUES ('monto_tipo_convenio', NEW.tipo_convenio_sena, 1, NEW.precio_estimado)
        ON DUPLICATE KEY UPDATE 
            cantidad = cantidad + 1,
            suma_total = suma_total + NEW.precio_estimado,
            fecha_actualizacion = CURRENT_TIMESTAMP;
    END IF;
    
    -- 8. Estadística: Por municipio (desde institución)
    IF NEW.nit_institucion IS NOT NULL THEN
        INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
        SELECT 'municipio_convenios', m.nom_municipio, 1
        FROM instituciones i
        JOIN municipio m ON i.id_municipio = m.id_municipio
        WHERE i.nit_institucion = NEW.nit_institucion
        ON DUPLICATE KEY UPDATE 
            cantidad = cantidad + 1,
            fecha_actualizacion = CURRENT_TIMESTAMP;
    END IF;
END$$

-- Trigger: UPDATE - Actualizar estadísticas al modificar convenio
DROP TRIGGER IF EXISTS tr_convenios_update_estadisticas$$
CREATE TRIGGER tr_convenios_update_estadisticas
AFTER UPDATE ON convenios
FOR EACH ROW
BEGIN
    -- 1. Actualizar: tipo_convenio_sena
    IF OLD.tipo_convenio_sena != NEW.tipo_convenio_sena 
       OR (OLD.tipo_convenio_sena IS NULL AND NEW.tipo_convenio_sena IS NOT NULL)
       OR (OLD.tipo_convenio_sena IS NOT NULL AND NEW.tipo_convenio_sena IS NULL) THEN
        
        IF OLD.tipo_convenio_sena IS NOT NULL THEN
            UPDATE estadistica_categoria 
            SET cantidad = GREATEST(cantidad - 1, 0),
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE categoria = 'tipo_convenio' AND nombre = OLD.tipo_convenio_sena;
        END IF;
        
        IF NEW.tipo_convenio_sena IS NOT NULL THEN
            INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
            VALUES ('tipo_convenio', NEW.tipo_convenio_sena, 1)
            ON DUPLICATE KEY UPDATE 
                cantidad = cantidad + 1,
                fecha_actualizacion = CURRENT_TIMESTAMP;
        END IF;
    END IF;
    
    -- 2. Actualizar: persona_apoyo_fpi
    IF OLD.persona_apoyo_fpi != NEW.persona_apoyo_fpi 
       OR (OLD.persona_apoyo_fpi IS NULL AND NEW.persona_apoyo_fpi IS NOT NULL)
       OR (OLD.persona_apoyo_fpi IS NOT NULL AND NEW.persona_apoyo_fpi IS NULL) THEN
        
        IF OLD.persona_apoyo_fpi IS NOT NULL THEN
            UPDATE estadistica_categoria 
            SET cantidad = GREATEST(cantidad - 1, 0),
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE categoria = 'persona_apoyo_fpi' AND nombre = OLD.persona_apoyo_fpi;
        END IF;
        
        IF NEW.persona_apoyo_fpi IS NOT NULL THEN
            INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
            VALUES ('persona_apoyo_fpi', NEW.persona_apoyo_fpi, 1)
            ON DUPLICATE KEY UPDATE 
                cantidad = cantidad + 1,
                fecha_actualizacion = CURRENT_TIMESTAMP;
        END IF;
    END IF;
    
    -- 3. Actualizar: estado_convenio
    IF OLD.estado_convenio != NEW.estado_convenio 
       OR (OLD.estado_convenio IS NULL AND NEW.estado_convenio IS NOT NULL)
       OR (OLD.estado_convenio IS NOT NULL AND NEW.estado_convenio IS NULL) THEN
        
        IF OLD.estado_convenio IS NOT NULL THEN
            UPDATE estadistica_categoria 
            SET cantidad = GREATEST(cantidad - 1, 0),
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE categoria = 'estado_convenio' AND nombre = OLD.estado_convenio;
        END IF;
        
        IF NEW.estado_convenio IS NOT NULL THEN
            INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
            VALUES ('estado_convenio', NEW.estado_convenio, 1)
            ON DUPLICATE KEY UPDATE 
                cantidad = cantidad + 1,
                fecha_actualizacion = CURRENT_TIMESTAMP;
        END IF;
    END IF;
    
    -- 4. Actualizar: tipo_proceso
    IF OLD.tipo_proceso != NEW.tipo_proceso 
       OR (OLD.tipo_proceso IS NULL AND NEW.tipo_proceso IS NOT NULL)
       OR (OLD.tipo_proceso IS NOT NULL AND NEW.tipo_proceso IS NULL) THEN
        
        IF OLD.tipo_proceso IS NOT NULL THEN
            UPDATE estadistica_categoria 
            SET cantidad = GREATEST(cantidad - 1, 0),
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE categoria = 'tipo_proceso' AND nombre = OLD.tipo_proceso;
        END IF;
        
        IF NEW.tipo_proceso IS NOT NULL THEN
            INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
            VALUES ('tipo_proceso', NEW.tipo_proceso, 1)
            ON DUPLICATE KEY UPDATE 
                cantidad = cantidad + 1,
                fecha_actualizacion = CURRENT_TIMESTAMP;
        END IF;
    END IF;
    
    -- 5. Actualizar: supervisor
    IF OLD.supervisor != NEW.supervisor 
       OR (OLD.supervisor IS NULL AND NEW.supervisor IS NOT NULL)
       OR (OLD.supervisor IS NOT NULL AND NEW.supervisor IS NULL) THEN
        
        IF OLD.supervisor IS NOT NULL THEN
            UPDATE estadistica_categoria 
            SET cantidad = GREATEST(cantidad - 1, 0),
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE categoria = 'supervisor' AND nombre = OLD.supervisor;
        END IF;
        
        IF NEW.supervisor IS NOT NULL THEN
            INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
            VALUES ('supervisor', NEW.supervisor, 1)
            ON DUPLICATE KEY UPDATE 
                cantidad = cantidad + 1,
                fecha_actualizacion = CURRENT_TIMESTAMP;
        END IF;
    END IF;
    
    -- 6. Actualizar: tipo_convenio general
    IF OLD.tipo_convenio != NEW.tipo_convenio 
       OR (OLD.tipo_convenio IS NULL AND NEW.tipo_convenio IS NOT NULL)
       OR (OLD.tipo_convenio IS NOT NULL AND NEW.tipo_convenio IS NULL) THEN
        
        IF OLD.tipo_convenio IS NOT NULL THEN
            UPDATE estadistica_categoria 
            SET cantidad = GREATEST(cantidad - 1, 0),
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE categoria = 'tipo_convenio_general' AND nombre = OLD.tipo_convenio;
        END IF;
        
        IF NEW.tipo_convenio IS NOT NULL THEN
            INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
            VALUES ('tipo_convenio_general', NEW.tipo_convenio, 1)
            ON DUPLICATE KEY UPDATE 
                cantidad = cantidad + 1,
                fecha_actualizacion = CURRENT_TIMESTAMP;
        END IF;
    END IF;
    
    -- 7. Actualizar: suma de montos por tipo_convenio_sena
    IF (OLD.precio_estimado != NEW.precio_estimado 
        OR OLD.precio_estimado IS NULL 
        OR NEW.precio_estimado IS NULL
        OR OLD.tipo_convenio_sena != NEW.tipo_convenio_sena) THEN
        
        -- Restar monto anterior
        IF OLD.precio_estimado IS NOT NULL AND OLD.tipo_convenio_sena IS NOT NULL THEN
            UPDATE estadistica_categoria 
            SET cantidad = GREATEST(cantidad - 1, 0),
                suma_total = GREATEST(suma_total - OLD.precio_estimado, 0),
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE categoria = 'monto_tipo_convenio' AND nombre = OLD.tipo_convenio_sena;
        END IF;
        
        -- Sumar nuevo monto
        IF NEW.precio_estimado IS NOT NULL AND NEW.tipo_convenio_sena IS NOT NULL THEN
            INSERT INTO estadistica_categoria (categoria, nombre, cantidad, suma_total)
            VALUES ('monto_tipo_convenio', NEW.tipo_convenio_sena, 1, NEW.precio_estimado)
            ON DUPLICATE KEY UPDATE 
                cantidad = cantidad + 1,
                suma_total = suma_total + NEW.precio_estimado,
                fecha_actualizacion = CURRENT_TIMESTAMP;
        END IF;
    END IF;
    
    -- 8. Actualizar: municipio si cambió institución
    IF OLD.nit_institucion != NEW.nit_institucion THEN
        -- Decrementar municipio anterior
        UPDATE estadistica_categoria ec
        JOIN instituciones i ON i.id_municipio IN (
            SELECT id_municipio FROM municipio WHERE nom_municipio = ec.nombre
        )
        SET ec.cantidad = GREATEST(ec.cantidad - 1, 0),
            ec.fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE ec.categoria = 'municipio_convenios' 
          AND i.nit_institucion = OLD.nit_institucion;
        
        -- Incrementar municipio nuevo
        INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
        SELECT 'municipio_convenios', m.nom_municipio, 1
        FROM instituciones i
        JOIN municipio m ON i.id_municipio = m.id_municipio
        WHERE i.nit_institucion = NEW.nit_institucion
        ON DUPLICATE KEY UPDATE 
            cantidad = cantidad + 1,
            fecha_actualizacion = CURRENT_TIMESTAMP;
    END IF;
END$$

-- Trigger: DELETE - Actualizar estadísticas al eliminar convenio
DROP TRIGGER IF EXISTS tr_convenios_delete_estadisticas$$
CREATE TRIGGER tr_convenios_delete_estadisticas
AFTER DELETE ON convenios
FOR EACH ROW
BEGIN
    -- 1. Decrementar: tipo_convenio_sena
    IF OLD.tipo_convenio_sena IS NOT NULL THEN
        UPDATE estadistica_categoria 
        SET cantidad = GREATEST(cantidad - 1, 0),
            fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE categoria = 'tipo_convenio' AND nombre = OLD.tipo_convenio_sena;
    END IF;
    
    -- 2. Decrementar: persona_apoyo_fpi
    IF OLD.persona_apoyo_fpi IS NOT NULL THEN
        UPDATE estadistica_categoria 
        SET cantidad = GREATEST(cantidad - 1, 0),
            fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE categoria = 'persona_apoyo_fpi' AND nombre = OLD.persona_apoyo_fpi;
    END IF;
    
    -- 3. Decrementar: estado_convenio
    IF OLD.estado_convenio IS NOT NULL THEN
        UPDATE estadistica_categoria 
        SET cantidad = GREATEST(cantidad - 1, 0),
            fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE categoria = 'estado_convenio' AND nombre = OLD.estado_convenio;
    END IF;
    
    -- 4. Decrementar: tipo_proceso
    IF OLD.tipo_proceso IS NOT NULL THEN
        UPDATE estadistica_categoria 
        SET cantidad = GREATEST(cantidad - 1, 0),
            fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE categoria = 'tipo_proceso' AND nombre = OLD.tipo_proceso;
    END IF;
    
    -- 5. Decrementar: supervisor
    IF OLD.supervisor IS NOT NULL THEN
        UPDATE estadistica_categoria 
        SET cantidad = GREATEST(cantidad - 1, 0),
            fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE categoria = 'supervisor' AND nombre = OLD.supervisor;
    END IF;
    
    -- 6. Decrementar: tipo_convenio general
    IF OLD.tipo_convenio IS NOT NULL THEN
        UPDATE estadistica_categoria 
        SET cantidad = GREATEST(cantidad - 1, 0),
            fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE categoria = 'tipo_convenio_general' AND nombre = OLD.tipo_convenio;
    END IF;
    
    -- 7. Restar monto
    IF OLD.precio_estimado IS NOT NULL AND OLD.tipo_convenio_sena IS NOT NULL THEN
        UPDATE estadistica_categoria 
        SET cantidad = GREATEST(cantidad - 1, 0),
            suma_total = GREATEST(suma_total - OLD.precio_estimado, 0),
            fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE categoria = 'monto_tipo_convenio' AND nombre = OLD.tipo_convenio_sena;
    END IF;
    
    -- 8. Decrementar: municipio
    IF OLD.nit_institucion IS NOT NULL THEN
        UPDATE estadistica_categoria ec
        JOIN instituciones i ON i.id_municipio IN (
            SELECT id_municipio FROM municipio WHERE nom_municipio = ec.nombre
        )
        SET ec.cantidad = GREATEST(ec.cantidad - 1, 0),
            ec.fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE ec.categoria = 'municipio_convenios' 
          AND i.nit_institucion = OLD.nit_institucion;
    END IF;
END$$

-- ------------------------------------------------------------
-- TRIGGERS PARA TABLA: homologacion - Estadísticas
-- Descripción: Actualizar estadísticas de homologaciones
-- ------------------------------------------------------------

-- Trigger: INSERT - Actualizar estadísticas al insertar homologación
DROP TRIGGER IF EXISTS tr_homologacion_insert_stats$$
CREATE TRIGGER tr_homologacion_insert_stats
AFTER INSERT ON homologacion
FOR EACH ROW
BEGIN
    -- 1. Estadística: Modalidad
    IF NEW.modalidad IS NOT NULL THEN
        INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
        VALUES ('modalidad_homologacion', NEW.modalidad, 1)
        ON DUPLICATE KEY UPDATE 
            cantidad = cantidad + 1,
            fecha_actualizacion = CURRENT_TIMESTAMP;
    END IF;
    
    -- 2. Estadística: Nivel de programa
    IF NEW.nivel_programa IS NOT NULL THEN
        INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
        VALUES ('nivel_programa', NEW.nivel_programa, 1)
        ON DUPLICATE KEY UPDATE 
            cantidad = cantidad + 1,
            fecha_actualizacion = CURRENT_TIMESTAMP;
    END IF;
    
    -- 3. Estadística: Regional
    IF NEW.regional IS NOT NULL THEN
        INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
        VALUES ('regional', NEW.regional, 1)
        ON DUPLICATE KEY UPDATE 
            cantidad = cantidad + 1,
            fecha_actualizacion = CURRENT_TIMESTAMP;
    END IF;
    
    -- 4. Estadística: Programa IES
    IF NEW.programa_ies IS NOT NULL THEN
        INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
        VALUES ('programa_ies', NEW.programa_ies, 1)
        ON DUPLICATE KEY UPDATE 
            cantidad = cantidad + 1,
            fecha_actualizacion = CURRENT_TIMESTAMP;
    END IF;
    
    -- 5. Estadística: Créditos promedio por modalidad
    IF NEW.creditos_homologados IS NOT NULL AND NEW.modalidad IS NOT NULL THEN
        INSERT INTO estadistica_categoria (categoria, nombre, cantidad, suma_total)
        VALUES ('creditos_por_modalidad', NEW.modalidad, 1, NEW.creditos_homologados)
        ON DUPLICATE KEY UPDATE 
            cantidad = cantidad + 1,
            suma_total = suma_total + NEW.creditos_homologados,
            fecha_actualizacion = CURRENT_TIMESTAMP;
    END IF;
END$$

-- Trigger: UPDATE - Actualizar estadísticas al modificar homologación
DROP TRIGGER IF EXISTS tr_homologacion_update_stats$$
CREATE TRIGGER tr_homologacion_update_stats
AFTER UPDATE ON homologacion
FOR EACH ROW
BEGIN
    -- 1. Actualizar: Modalidad
    IF OLD.modalidad != NEW.modalidad 
       OR (OLD.modalidad IS NULL AND NEW.modalidad IS NOT NULL)
       OR (OLD.modalidad IS NOT NULL AND NEW.modalidad IS NULL) THEN
        
        IF OLD.modalidad IS NOT NULL THEN
            UPDATE estadistica_categoria 
            SET cantidad = GREATEST(cantidad - 1, 0),
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE categoria = 'modalidad_homologacion' AND nombre = OLD.modalidad;
        END IF;
        
        IF NEW.modalidad IS NOT NULL THEN
            INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
            VALUES ('modalidad_homologacion', NEW.modalidad, 1)
            ON DUPLICATE KEY UPDATE 
                cantidad = cantidad + 1,
                fecha_actualizacion = CURRENT_TIMESTAMP;
        END IF;
    END IF;
    
    -- 2. Actualizar: Nivel programa
    IF OLD.nivel_programa != NEW.nivel_programa 
       OR (OLD.nivel_programa IS NULL AND NEW.nivel_programa IS NOT NULL)
       OR (OLD.nivel_programa IS NOT NULL AND NEW.nivel_programa IS NULL) THEN
        
        IF OLD.nivel_programa IS NOT NULL THEN
            UPDATE estadistica_categoria 
            SET cantidad = GREATEST(cantidad - 1, 0),
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE categoria = 'nivel_programa' AND nombre = OLD.nivel_programa;
        END IF;
        
        IF NEW.nivel_programa IS NOT NULL THEN
            INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
            VALUES ('nivel_programa', NEW.nivel_programa, 1)
            ON DUPLICATE KEY UPDATE 
                cantidad = cantidad + 1,
                fecha_actualizacion = CURRENT_TIMESTAMP;
        END IF;
    END IF;
    
    -- 3. Actualizar: Regional
    IF OLD.regional != NEW.regional 
       OR (OLD.regional IS NULL AND NEW.regional IS NOT NULL)
       OR (OLD.regional IS NOT NULL AND NEW.regional IS NULL) THEN
        
        IF OLD.regional IS NOT NULL THEN
            UPDATE estadistica_categoria 
            SET cantidad = GREATEST(cantidad - 1, 0),
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE categoria = 'regional' AND nombre = OLD.regional;
        END IF;
        
        IF NEW.regional IS NOT NULL THEN
            INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
            VALUES ('regional', NEW.regional, 1)
            ON DUPLICATE KEY UPDATE 
                cantidad = cantidad + 1,
                fecha_actualizacion = CURRENT_TIMESTAMP;
        END IF;
    END IF;
    
    -- 4. Actualizar: Programa IES
    IF OLD.programa_ies != NEW.programa_ies 
       OR (OLD.programa_ies IS NULL AND NEW.programa_ies IS NOT NULL)
       OR (OLD.programa_ies IS NOT NULL AND NEW.programa_ies IS NULL) THEN
        
        IF OLD.programa_ies IS NOT NULL THEN
            UPDATE estadistica_categoria 
            SET cantidad = GREATEST(cantidad - 1, 0),
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE categoria = 'programa_ies' AND nombre = OLD.programa_ies;
        END IF;
        
        IF NEW.programa_ies IS NOT NULL THEN
            INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
            VALUES ('programa_ies', NEW.programa_ies, 1)
            ON DUPLICATE KEY UPDATE 
                cantidad = cantidad + 1,
                fecha_actualizacion = CURRENT_TIMESTAMP;
        END IF;
    END IF;
    
    -- 5. Actualizar: Créditos por modalidad
    IF (OLD.creditos_homologados != NEW.creditos_homologados 
        OR OLD.creditos_homologados IS NULL 
        OR NEW.creditos_homologados IS NULL
        OR OLD.modalidad != NEW.modalidad) THEN
        
        -- Restar créditos anteriores
        IF OLD.creditos_homologados IS NOT NULL AND OLD.modalidad IS NOT NULL THEN
            UPDATE estadistica_categoria 
            SET cantidad = GREATEST(cantidad - 1, 0),
                suma_total = GREATEST(suma_total - OLD.creditos_homologados, 0),
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE categoria = 'creditos_por_modalidad' AND nombre = OLD.modalidad;
        END IF;
        
        -- Sumar nuevos créditos
        IF NEW.creditos_homologados IS NOT NULL AND NEW.modalidad IS NOT NULL THEN
            INSERT INTO estadistica_categoria (categoria, nombre, cantidad, suma_total)
            VALUES ('creditos_por_modalidad', NEW.modalidad, 1, NEW.creditos_homologados)
            ON DUPLICATE KEY UPDATE 
                cantidad = cantidad + 1,
                suma_total = suma_total + NEW.creditos_homologados,
                fecha_actualizacion = CURRENT_TIMESTAMP;
        END IF;
    END IF;
END$$

-- Trigger: DELETE - Actualizar estadísticas al eliminar homologación
DROP TRIGGER IF EXISTS tr_homologacion_delete_stats$$
CREATE TRIGGER tr_homologacion_delete_stats
AFTER DELETE ON homologacion
FOR EACH ROW
BEGIN
    -- 1. Decrementar: Modalidad
    IF OLD.modalidad IS NOT NULL THEN
        UPDATE estadistica_categoria 
        SET cantidad = GREATEST(cantidad - 1, 0),
            fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE categoria = 'modalidad_homologacion' AND nombre = OLD.modalidad;
    END IF;
    
    -- 2. Decrementar: Nivel programa
    IF OLD.nivel_programa IS NOT NULL THEN
        UPDATE estadistica_categoria 
        SET cantidad = GREATEST(cantidad - 1, 0),
            fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE categoria = 'nivel_programa' AND nombre = OLD.nivel_programa;
    END IF;
    
    -- 3. Decrementar: Regional
    IF OLD.regional IS NOT NULL THEN
        UPDATE estadistica_categoria 
        SET cantidad = GREATEST(cantidad - 1, 0),
            fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE categoria = 'regional' AND nombre = OLD.regional;
    END IF;
    
    -- 4. Decrementar: Programa IES
    IF OLD.programa_ies IS NOT NULL THEN
        UPDATE estadistica_categoria 
        SET cantidad = GREATEST(cantidad - 1, 0),
            fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE categoria = 'programa_ies' AND nombre = OLD.programa_ies;
    END IF;
    
    -- 5. Restar créditos
    IF OLD.creditos_homologados IS NOT NULL AND OLD.modalidad IS NOT NULL THEN
        UPDATE estadistica_categoria 
        SET cantidad = GREATEST(cantidad - 1, 0),
            suma_total = GREATEST(suma_total - OLD.creditos_homologados, 0),
            fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE categoria = 'creditos_por_modalidad' AND nombre = OLD.modalidad;
    END IF;
END$$

DELIMITER ;


-- ============================================================
-- SECCIÓN 3: VISTAS
-- ============================================================

-- ------------------------------------------------------------
-- Vista: v_resumen_estadisticas
-- Descripción: Resumen general de estadísticas por categoría
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW v_resumen_estadisticas AS
SELECT 
    categoria,
    COUNT(*) as total_items,
    SUM(cantidad) as suma_cantidades,
    SUM(suma_total) as suma_montos,
    MAX(fecha_actualizacion) as ultima_actualizacion
FROM estadistica_categoria
GROUP BY categoria
ORDER BY categoria;

-- ------------------------------------------------------------
-- Vista: v_top_instituciones
-- Descripción: Top instituciones ordenadas por cantidad de convenios
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW v_top_instituciones AS
SELECT 
    i.nit_institucion,
    i.nombre_institucion,
    i.cant_convenios,
    m.nom_municipio,
    COALESCE(SUM(c.precio_estimado), 0) as monto_total_convenios,
    COUNT(DISTINCT c.id_convenio) as total_convenios_activos
FROM instituciones i
LEFT JOIN convenios c ON i.nit_institucion = c.nit_institucion
LEFT JOIN municipio m ON i.id_municipio = m.id_municipio
GROUP BY i.nit_institucion, i.nombre_institucion, i.cant_convenios, m.nom_municipio
ORDER BY i.cant_convenios DESC, monto_total_convenios DESC;

-- ------------------------------------------------------------
-- Vista: v_carga_supervisores
-- Descripción: Carga de trabajo de supervisores de convenios
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW v_carga_supervisores AS
SELECT 
    supervisor,
    COUNT(*) as total_convenios,
    SUM(CASE WHEN estado_convenio = 'Activo' THEN 1 ELSE 0 END) as convenios_activos,
    SUM(CASE WHEN estado_convenio = 'Finalizado' THEN 1 ELSE 0 END) as convenios_finalizados,
    COALESCE(SUM(precio_estimado), 0) as monto_total_supervisado,
    COALESCE(AVG(precio_estimado), 0) as monto_promedio
FROM convenios
WHERE supervisor IS NOT NULL
GROUP BY supervisor
ORDER BY total_convenios DESC, monto_total_supervisado DESC;

-- ------------------------------------------------------------
-- Vista: v_convenios_por_municipio
-- Descripción: Distribución de convenios por municipio
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW v_convenios_por_municipio AS
SELECT 
    m.id_municipio,
    m.nom_municipio,
    COUNT(DISTINCT i.nit_institucion) as total_instituciones,
    COUNT(c.id_convenio) as total_convenios,
    COALESCE(SUM(c.precio_estimado), 0) as monto_total
FROM municipio m
LEFT JOIN instituciones i ON m.id_municipio = i.id_municipio
LEFT JOIN convenios c ON i.nit_institucion = c.nit_institucion
GROUP BY m.id_municipio, m.nom_municipio
ORDER BY total_convenios DESC, monto_total DESC;

-- ------------------------------------------------------------
-- Vista: v_resumen_homologaciones
-- Descripción: Resumen de homologaciones por institución
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW v_resumen_homologaciones AS
SELECT 
    i.nit_institucion,
    i.nombre_institucion,
    COUNT(h.id_homologacion) as total_homologaciones,
    SUM(h.creditos_homologados) as total_creditos_homologados,
    AVG(h.creditos_homologados) as promedio_creditos,
    COUNT(DISTINCT h.modalidad) as modalidades_diferentes,
    COUNT(DISTINCT h.nivel_programa) as niveles_diferentes
FROM instituciones i
LEFT JOIN homologacion h ON i.nit_institucion = h.nit_institucion_destino
GROUP BY i.nit_institucion, i.nombre_institucion
ORDER BY total_homologaciones DESC;

-- ------------------------------------------------------------
-- Vista: v_estadisticas_convenios_activos
-- Descripción: Estadísticas de convenios activos
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW v_estadisticas_convenios_activos AS
SELECT 
    tipo_convenio_sena,
    COUNT(*) as cantidad_activos,
    SUM(precio_estimado) as monto_total,
    AVG(precio_estimado) as monto_promedio,
    MIN(fecha_firma) as fecha_primer_convenio,
    MAX(fecha_firma) as fecha_ultimo_convenio,
    COUNT(DISTINCT supervisor) as supervisores_distintos
FROM convenios
WHERE estado_convenio = 'Activo'
GROUP BY tipo_convenio_sena
ORDER BY cantidad_activos DESC;


-- ============================================================
-- SECCIÓN 4: PROCEDIMIENTOS ALMACENADOS
-- ============================================================

DELIMITER $$

-- ------------------------------------------------------------
-- Procedimiento: sp_recalcular_estadisticas
-- Descripción: Recalcula todas las estadísticas desde cero
-- ------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_recalcular_estadisticas$$

CREATE PROCEDURE sp_recalcular_estadisticas()
BEGIN
    DECLARE total_registros INT DEFAULT 0;
    
    -- Limpiar estadísticas actuales
    TRUNCATE TABLE estadistica_categoria;
    
    -- 1. Recalcular estadísticas de CONVENIOS
    
    -- tipo_convenio_sena
    INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
    SELECT 'tipo_convenio', tipo_convenio_sena, COUNT(*)
    FROM convenios
    WHERE tipo_convenio_sena IS NOT NULL
    GROUP BY tipo_convenio_sena;
    
    -- persona_apoyo_fpi
    INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
    SELECT 'persona_apoyo_fpi', persona_apoyo_fpi, COUNT(*)
    FROM convenios
    WHERE persona_apoyo_fpi IS NOT NULL
    GROUP BY persona_apoyo_fpi;
    
    -- estado_convenio
    INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
    SELECT 'estado_convenio', estado_convenio, COUNT(*)
    FROM convenios
    WHERE estado_convenio IS NOT NULL
    GROUP BY estado_convenio;
    
    -- tipo_proceso
    INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
    SELECT 'tipo_proceso', tipo_proceso, COUNT(*)
    FROM convenios
    WHERE tipo_proceso IS NOT NULL
    GROUP BY tipo_proceso;
    
    -- supervisor
    INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
    SELECT 'supervisor', supervisor, COUNT(*)
    FROM convenios
    WHERE supervisor IS NOT NULL
    GROUP BY supervisor;
    
    -- tipo_convenio general
    INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
    SELECT 'tipo_convenio_general', tipo_convenio, COUNT(*)
    FROM convenios
    WHERE tipo_convenio IS NOT NULL
    GROUP BY tipo_convenio;
    
    -- Montos por tipo de convenio
    INSERT INTO estadistica_categoria (categoria, nombre, cantidad, suma_total)
    SELECT 'monto_tipo_convenio', tipo_convenio_sena, COUNT(*), SUM(precio_estimado)
    FROM convenios
    WHERE tipo_convenio_sena IS NOT NULL AND precio_estimado IS NOT NULL
    GROUP BY tipo_convenio_sena;
    
    -- Convenios por municipio
    INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
    SELECT 'municipio_convenios', m.nom_municipio, COUNT(c.id_convenio)
    FROM municipio m
    JOIN instituciones i ON m.id_municipio = i.id_municipio
    JOIN convenios c ON i.nit_institucion = c.nit_institucion
    GROUP BY m.nom_municipio;
    
    -- 2. Recalcular estadísticas de HOMOLOGACIONES
    
    -- Modalidad
    INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
    SELECT 'modalidad_homologacion', modalidad, COUNT(*)
    FROM homologacion
    WHERE modalidad IS NOT NULL
    GROUP BY modalidad;
    
    -- Nivel programa
    INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
    SELECT 'nivel_programa', nivel_programa, COUNT(*)
    FROM homologacion
    WHERE nivel_programa IS NOT NULL
    GROUP BY nivel_programa;
    
    -- Regional
    INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
    SELECT 'regional', regional, COUNT(*)
    FROM homologacion
    WHERE regional IS NOT NULL
    GROUP BY regional;
    
    -- Programa IES
    INSERT INTO estadistica_categoria (categoria, nombre, cantidad)
    SELECT 'programa_ies', programa_ies, COUNT(*)
    FROM homologacion
    WHERE programa_ies IS NOT NULL
    GROUP BY programa_ies;
    
    -- Créditos por modalidad
    INSERT INTO estadistica_categoria (categoria, nombre, cantidad, suma_total)
    SELECT 'creditos_por_modalidad', modalidad, COUNT(*), SUM(creditos_homologados)
    FROM homologacion
    WHERE modalidad IS NOT NULL AND creditos_homologados IS NOT NULL
    GROUP BY modalidad;
    
    -- Obtener total de registros creados
    SELECT COUNT(*) INTO total_registros FROM estadistica_categoria;
    
    -- Retornar mensaje de éxito
    SELECT 
        'Estadísticas recalculadas exitosamente' as mensaje,
        total_registros as total_registros_estadisticas,
        NOW() as fecha_recalculo;
END$$

-- ------------------------------------------------------------
-- Procedimiento: sp_resumen_estadisticas_generales
-- Descripción: Obtiene un resumen general de todas las estadísticas
-- ------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_resumen_estadisticas_generales$$

CREATE PROCEDURE sp_resumen_estadisticas_generales()
BEGIN
    SELECT 
        'RESUMEN GENERAL DEL SISTEMA' as seccion,
        '=========================' as separador;
    
    SELECT 
        'Total Instituciones' as metrica,
        COUNT(*) as valor
    FROM instituciones
    UNION ALL
    SELECT 
        'Total Convenios' as metrica,
        COUNT(*) as valor
    FROM convenios
    UNION ALL
    SELECT 
        'Total Homologaciones' as metrica,
        COUNT(*) as valor
    FROM homologacion
    UNION ALL
    SELECT 
        'Monto Total Convenios' as metrica,
        COALESCE(SUM(precio_estimado), 0) as valor
    FROM convenios;
    
    -- Mostrar resumen por categoría
    SELECT * FROM v_resumen_estadisticas;
END$$

-- ------------------------------------------------------------
-- Procedimiento: sp_estadisticas_por_categoria
-- Descripción: Obtiene estadísticas detalladas de una categoría específica
-- ------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_estadisticas_por_categoria$$

CREATE PROCEDURE sp_estadisticas_por_categoria(IN p_categoria VARCHAR(50))
BEGIN
    IF p_categoria IS NULL OR p_categoria = '' THEN
        SELECT 'Error: Debe proporcionar una categoría válida' as mensaje;
    ELSE
        SELECT 
            categoria,
            nombre,
            cantidad,
            suma_total,
            fecha_actualizacion
        FROM estadistica_categoria
        WHERE categoria = p_categoria
        ORDER BY cantidad DESC, nombre ASC;
    END IF;
END$$

DELIMITER ;


-- ============================================================
-- SECCIÓN 5: INSERTS - DATOS INICIALES
-- ============================================================

-- ------------------------------------------------------------
-- Insertar ROLES
-- ------------------------------------------------------------
INSERT INTO rol (nombre_rol) VALUES
('Admin'),
('Aprendiz'),
('Supervisor'),
('Coordinador');

-- ------------------------------------------------------------
-- Insertar MUNICIPIOS
-- ------------------------------------------------------------
INSERT INTO municipio (id_municipio, nom_municipio) VALUES
('57066001','Pereira'),
('57066045','Apía'),
('57066075','Balboa'),
('57066088','Belén de Umbría'),
('57066170','Dosquebradas'),
('57066320','Guática'),
('57066383','La Celia'),
('57066388','La Virginia'),
('57066430','Marsella'),
('57066460','Mistrató'),
('57066511','Pueblo Rico'),
('57066535','Quinchía'),
('57066685','Santa Rosa de Cabal'),
('57066740','Santuario');

-- ------------------------------------------------------------
-- Insertar INSTITUCIONES
-- ------------------------------------------------------------
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

-- ------------------------------------------------------------
-- Insertar ESTADÍSTICAS INICIALES (categorías predefinidas)
-- ------------------------------------------------------------
INSERT INTO estadistica_categoria (categoria, nombre, cantidad) VALUES
-- Tipos de convenio
('tipo_convenio', 'Interadministrativo', 0),
('tipo_convenio', 'Cooperación Técnica', 0),
('tipo_convenio', 'Docencia-Servicio', 0),

-- Personas de apoyo FPI
('persona_apoyo_fpi', 'Angie Tatiana Rengifo', 0),
('persona_apoyo_fpi', 'Angela María Lara', 0),
('persona_apoyo_fpi', 'Yolanda Agudelo', 0),

-- Estados de convenio
('estado_convenio', 'Activo', 0),
('estado_convenio', 'Finalizado', 0),
('estado_convenio', 'En proceso', 0),
('estado_convenio', 'Suspendido', 0),

-- Tipos de proceso
('tipo_proceso', 'Licitación Pública', 0),
('tipo_proceso', 'Contratación Directa', 0),
('tipo_proceso', 'Selección Abreviada', 0),
('tipo_proceso', 'Concurso de Méritos', 0),

-- Modalidades de homologación
('modalidad_homologacion', 'Presencial', 0),
('modalidad_homologacion', 'Virtual', 0),
('modalidad_homologacion', 'Mixta', 0),

-- Niveles de programa
('nivel_programa', 'Tecnólogo', 0),
('nivel_programa', 'Técnico', 0),
('nivel_programa', 'Especialización', 0);


