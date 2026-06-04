-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 04-06-2026 a las 01:02:10
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `asistencia`
--

DELIMITER $$
--
-- Procedimientos
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `generar_nuevo_qr` ()   BEGIN

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

END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alumnos`
--

CREATE TABLE `alumnos` (
  `id_alumno` int(11) NOT NULL,
  `matricula` varchar(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido_paterno` varchar(100) NOT NULL,
  `apellido_materno` varchar(100) DEFAULT NULL,
  `grado` varchar(20) DEFAULT NULL,
  `grupo` varchar(10) DEFAULT NULL,
  `correo` varchar(150) DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `alumnos`
--

INSERT INTO `alumnos` (`id_alumno`, `matricula`, `nombre`, `apellido_paterno`, `apellido_materno`, `grado`, `grupo`, `correo`, `fecha_registro`, `password`) VALUES
(1, '23308060610457', 'Anette', 'Michel', 'Leonardo', '5', 'D', 'alumno@cetis61.edu.mx', '2026-05-22 21:19:34', ''),
(4, '123456789', 'anette', '', NULL, NULL, NULL, 'zeferinoo.anette@gmail.com', '2026-05-26 00:10:36', '$2b$12$.F5eUgf1zO8gf6r42m70VebE2mQoMzo5.W1GBviH10Zpff37HY/li'),
(5, 'DOCENTE', 'Laura', '', NULL, NULL, NULL, 'anetleo9@gmail.com', '2026-05-26 22:57:12', '$2b$12$aQmifRYrJfj1XI8pp5ClDu7NjiEZR7NIYrOhYJGkPv1Egc47wVLRC');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistencia`
--

CREATE TABLE `asistencia` (
  `id_asistencia` int(11) NOT NULL,
  `id_alumno` int(11) NOT NULL,
  `id_qr` int(11) NOT NULL,
  `fecha_hora` datetime DEFAULT current_timestamp(),
  `estado` enum('PRESENTE','RETARDO','FALTA') DEFAULT 'PRESENTE',
  `matricula` varchar(20) NOT NULL,
  `fecha` date DEFAULT NULL,
  `hora` time DEFAULT NULL,
  `estatus` varchar(20) DEFAULT 'Presente'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `asistencia`
--

INSERT INTO `asistencia` (`id_asistencia`, `id_alumno`, `id_qr`, `fecha_hora`, `estado`, `matricula`, `fecha`, `hora`, `estatus`) VALUES
(2, 4, 3, '2026-06-03 17:00:38', 'PRESENTE', '123456789', '2026-06-03', '17:00:38', 'Presente');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `codigos_qr`
--

CREATE TABLE `codigos_qr` (
  `id_qr` int(11) NOT NULL,
  `codigo` varchar(255) NOT NULL,
  `fecha_generacion` datetime DEFAULT current_timestamp(),
  `fecha_expiracion` datetime NOT NULL,
  `activo` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `codigos_qr`
--

INSERT INTO `codigos_qr` (`id_qr`, `codigo`, `fecha_generacion`, `fecha_expiracion`, `activo`) VALUES
(1, 'QR-b476059b-53d1-11f1-be0b-00d49e774a74-20260519162556', '2026-05-19 16:25:56', '2026-05-19 17:25:56', 0),
(2, 'QR-b47e1424-53d1-11f1-be0b-00d49e774a74-20260519162556', '2026-05-19 16:25:56', '2026-05-19 17:25:56', 0),
(3, 'QR-15e179f3-53da-11f1-be0b-00d49e774a74-20260519172556', '2026-05-19 17:25:56', '2026-05-19 18:25:56', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contenido`
--

CREATE TABLE `contenido` (
  `id_contenido` int(11) NOT NULL,
  `título` varchar(150) NOT NULL,
  `descripción` text DEFAULT NULL,
  `año_lanzamiento` year(4) DEFAULT NULL,
  `clasificación` varchar(20) DEFAULT NULL,
  `duración` int(11) DEFAULT NULL,
  `tipo_contenido` enum('Película','Serie') NOT NULL,
  `imagen_portada` varchar(255) DEFAULT NULL,
  `género` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `disponibilidad`
--

CREATE TABLE `disponibilidad` (
  `id_disponibilidad` int(11) NOT NULL,
  `id_contenido` int(11) NOT NULL,
  `id_plataforma` int(11) NOT NULL,
  `visualización_del_enlace` varchar(500) DEFAULT NULL,
  `calidad` varchar(50) DEFAULT NULL,
  `idioma` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `favoritos`
--

CREATE TABLE `favoritos` (
  `id_favorito` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_contenido` int(11) NOT NULL,
  `fecha_agregado` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial_qr`
--

CREATE TABLE `historial_qr` (
  `id_historial` int(11) NOT NULL,
  `codigo_anterior` varchar(255) DEFAULT NULL,
  `fecha_cambio` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `historial_qr`
--

INSERT INTO `historial_qr` (`id_historial`, `codigo_anterior`, `fecha_cambio`) VALUES
(1, 'QR-b476059b-53d1-11f1-be0b-00d49e774a74-20260519162556', '2026-05-19 16:25:56'),
(2, 'QR-b47e1424-53d1-11f1-be0b-00d49e774a74-20260519162556', '2026-05-19 17:25:56');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `plataforma_streaming`
--

CREATE TABLE `plataforma_streaming` (
  `id_plataforma` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `url_principal` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `fecha_registro` date DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_usuario`, `nombre`, `fecha_registro`, `email`, `apellido`, `password`) VALUES
(1, 'Anette Michel', '2026-05-13', 'anette@gmail.com', 'Zeferino Leonardo', '$2b$12$TxdiTbPQHvqcdeNdBCe2Au32mmwrogGoTTCz9L.B26qYevFrZNHDm');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` enum('ADMIN','DOCENTE') DEFAULT 'DOCENTE',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `correo`, `password`, `rol`, `fecha_creacion`) VALUES
(1, 'anette', '23308060610457@cetis61.edu.mx', '$2b$12$1cvMNAgfDd.5Ro20ewFfH./KbOfpD86FkCTZsuZGXEiVn7DWHWYdO', 'DOCENTE', '2026-05-22 21:05:00'),
(2, 'Anette', 'zeferinoo.anette@gmail.com', '$2b$12$cbluo227jah1Mqpm2ot7.OxKshc3IphgynIFUuK5R.QhoTRA0IrJK', 'DOCENTE', '2026-05-23 18:10:26');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alumnos`
--
ALTER TABLE `alumnos`
  ADD PRIMARY KEY (`id_alumno`),
  ADD UNIQUE KEY `matricula` (`matricula`);

--
-- Indices de la tabla `asistencia`
--
ALTER TABLE `asistencia`
  ADD PRIMARY KEY (`id_asistencia`),
  ADD KEY `id_alumno` (`id_alumno`),
  ADD KEY `id_qr` (`id_qr`);

--
-- Indices de la tabla `codigos_qr`
--
ALTER TABLE `codigos_qr`
  ADD PRIMARY KEY (`id_qr`),
  ADD UNIQUE KEY `codigo` (`codigo`);

--
-- Indices de la tabla `contenido`
--
ALTER TABLE `contenido`
  ADD PRIMARY KEY (`id_contenido`);

--
-- Indices de la tabla `disponibilidad`
--
ALTER TABLE `disponibilidad`
  ADD PRIMARY KEY (`id_disponibilidad`),
  ADD KEY `fk_disponibilidad_contenido` (`id_contenido`),
  ADD KEY `fk_disponibilidad_plataforma` (`id_plataforma`);

--
-- Indices de la tabla `favoritos`
--
ALTER TABLE `favoritos`
  ADD PRIMARY KEY (`id_favorito`),
  ADD KEY `fk_favoritos_usuario` (`id_usuario`),
  ADD KEY `fk_favoritos_contenido` (`id_contenido`);

--
-- Indices de la tabla `historial_qr`
--
ALTER TABLE `historial_qr`
  ADD PRIMARY KEY (`id_historial`);

--
-- Indices de la tabla `plataforma_streaming`
--
ALTER TABLE `plataforma_streaming`
  ADD PRIMARY KEY (`id_plataforma`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alumnos`
--
ALTER TABLE `alumnos`
  MODIFY `id_alumno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `asistencia`
--
ALTER TABLE `asistencia`
  MODIFY `id_asistencia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `codigos_qr`
--
ALTER TABLE `codigos_qr`
  MODIFY `id_qr` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `contenido`
--
ALTER TABLE `contenido`
  MODIFY `id_contenido` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `disponibilidad`
--
ALTER TABLE `disponibilidad`
  MODIFY `id_disponibilidad` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `favoritos`
--
ALTER TABLE `favoritos`
  MODIFY `id_favorito` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `historial_qr`
--
ALTER TABLE `historial_qr`
  MODIFY `id_historial` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `plataforma_streaming`
--
ALTER TABLE `plataforma_streaming`
  MODIFY `id_plataforma` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asistencia`
--
ALTER TABLE `asistencia`
  ADD CONSTRAINT `asistencia_ibfk_1` FOREIGN KEY (`id_alumno`) REFERENCES `alumnos` (`id_alumno`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `asistencia_ibfk_2` FOREIGN KEY (`id_qr`) REFERENCES `codigos_qr` (`id_qr`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `disponibilidad`
--
ALTER TABLE `disponibilidad`
  ADD CONSTRAINT `fk_disponibilidad_contenido` FOREIGN KEY (`id_contenido`) REFERENCES `contenido` (`id_contenido`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_disponibilidad_plataforma` FOREIGN KEY (`id_plataforma`) REFERENCES `plataforma_streaming` (`id_plataforma`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `favoritos`
--
ALTER TABLE `favoritos`
  ADD CONSTRAINT `fk_favoritos_contenido` FOREIGN KEY (`id_contenido`) REFERENCES `contenido` (`id_contenido`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_favoritos_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;

DELIMITER $$
--
-- Eventos
--
CREATE DEFINER=`root`@`localhost` EVENT `evento_generar_qr` ON SCHEDULE EVERY 1 HOUR STARTS '2026-05-19 16:25:56' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN
    CALL generar_nuevo_qr();
END$$

DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
