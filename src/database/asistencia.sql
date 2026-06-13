-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.4.32-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.13.0.7147
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para asistencia
CREATE DATABASE IF NOT EXISTS `asistencia` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `asistencia`;

-- Volcando estructura para tabla asistencia.alumnos
CREATE TABLE IF NOT EXISTS `alumnos` (
  `id_alumno` int(11) AUTO_INCREMENT,
  `matricula` varchar(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido_paterno` varchar(100) NOT NULL,
  `apellido_materno` varchar(100) DEFAULT NULL,
  `grado` varchar(20) DEFAULT NULL,
  `grupo` varchar(10) DEFAULT NULL,
  `correo` varchar(150) DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id_alumno`),
  UNIQUE KEY `matricula` (`matricula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla asistencia.alumnos: ~0 rows (aproximadamente)
DELETE FROM `alumnos`;

-- Volcando estructura para tabla asistencia.asistencia
CREATE TABLE IF NOT EXISTS `asistencia` (
  `id_asistencia` int(11) AUTO_INCREMENT,
  `id_alumno` int(11) NOT NULL,
  `id_qr` int(11) NOT NULL,
  `fecha_hora` datetime DEFAULT current_timestamp(),
  `estado` enum('PRESENTE','RETARDO','FALTA') DEFAULT 'PRESENTE',
  `matricula` varchar(20) NOT NULL,
  `fecha` date DEFAULT NULL,
  `hora` time DEFAULT NULL,
  `estatus` varchar(20) DEFAULT 'Presente',
  PRIMARY KEY (`id_asistencia`),
  KEY `id_alumno` (`id_alumno`),
  KEY `id_qr` (`id_qr`),
  CONSTRAINT `asistencia_ibfk_1` FOREIGN KEY (`id_alumno`) REFERENCES `alumnos` (`id_alumno`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `asistencia_ibfk_2` FOREIGN KEY (`id_qr`) REFERENCES `codigos_qr` (`id_qr`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla asistencia.asistencia: ~0 rows (aproximadamente)
DELETE FROM `asistencia`;

-- Volcando estructura para tabla asistencia.codigos_qr
CREATE TABLE IF NOT EXISTS `codigos_qr` (
  `id_qr` int(11) AUTO_INCREMENT,
  `codigo` varchar(255) NOT NULL,
  `fecha_generacion` datetime DEFAULT current_timestamp(),
  `fecha_expiracion` datetime NOT NULL,
  `activo` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id_qr`),
  UNIQUE KEY `codigo` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla asistencia.codigos_qr: ~0 rows (aproximadamente)
DELETE FROM `codigos_qr`;

-- Volcando estructura para evento asistencia.evento_generar_qr
DELIMITER //
CREATE EVENT `evento_generar_qr` ON SCHEDULE EVERY 3 MINUTE STARTS '2026-05-19 16:25:56' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN
    CALL generar_nuevo_qr();
END//
DELIMITER ;

-- Volcando estructura para procedimiento asistencia.generar_nuevo_qr
DELIMITER //
CREATE PROCEDURE `generar_nuevo_qr`()
BEGIN

    INSERT INTO historial_qr(codigo_anterior)
    SELECT codigo
    FROM codigos_qr
    WHERE activo = TRUE;

    UPDATE codigos_qr
    SET activo = FALSE
    WHERE activo = TRUE;

    INSERT INTO codigos_qr(
        codigo,
        fecha_expiracion,
        activo
    )
    VALUES(
        CONCAT(
            'QR-',
            UUID(),
            '-',
            DATE_FORMAT(NOW(), '%Y%m%d%H%i%s')
        ),
        DATE_ADD(NOW(), INTERVAL 1 HOUR),
        TRUE
    );

END//
DELIMITER ;

-- Volcando estructura para tabla asistencia.historial_qr
CREATE TABLE IF NOT EXISTS `historial_qr` (
  `id_historial` int(11) AUTO_INCREMENT,
  `codigo_anterior` varchar(255) DEFAULT NULL,
  `fecha_cambio` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id_historial`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla asistencia.historial_qr: ~0 rows (aproximadamente)
DELETE FROM `historial_qr`;

-- Volcando estructura para tabla asistencia.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id_usuario` int(11) AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` enum('ADMIN','DOCENTE') DEFAULT 'DOCENTE',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla asistencia.usuarios: ~0 rows (aproximadamente)
DELETE FROM `usuarios`;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
