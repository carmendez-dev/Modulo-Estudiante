-- Script SQL para crear las tablas de Cursos e Inscripciones
-- Ejecutar este script en phpMyAdmin o MySQL

USE bienestar_estudiantil;

-- Crear tabla de cursos
CREATE TABLE IF NOT EXISTS `cursos` (
  `id_curso` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nombre_curso` varchar(100) NOT NULL,
  `nivel` enum('inicial', 'primaria', 'secundaria') NOT NULL,
  `gestion` varchar(10) NOT NULL,
  INDEX `idx_nivel` (`nivel`),
  INDEX `idx_gestion` (`gestion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Crear tabla de asociación estudiantes_cursos (relación many-to-many)
CREATE TABLE IF NOT EXISTS `estudiantes_cursos` (
  `id_estudiante` int(11) NOT NULL,
  `id_curso` int(11) NOT NULL,
  PRIMARY KEY (`id_estudiante`, `id_curso`),
  CONSTRAINT `fk_estudiantes_cursos_estudiante`
    FOREIGN KEY (`id_estudiante`)
    REFERENCES `estudiantes` (`id_estudiante`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_estudiantes_cursos_curso`
    FOREIGN KEY (`id_curso`)
    REFERENCES `cursos` (`id_curso`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Datos de ejemplo para cursos
INSERT INTO `cursos` (`nombre_curso`, `nivel`, `gestion`) VALUES
('Prekinder A', 'inicial', '2024'),
('Kinder B', 'inicial', '2024'),
('Primero A', 'primaria', '2024'),
('Segundo B', 'primaria', '2024'),
('Tercero A', 'primaria', '2024'),
('Cuarto B', 'primaria', '2024'),
('Quinto A', 'primaria', '2024'),
('Sexto B', 'primaria', '2024'),
('Primero Sec A', 'secundaria', '2024'),
('Segundo Sec B', 'secundaria', '2024'),
('Tercero Sec A', 'secundaria', '2024'),
('Cuarto Sec B', 'secundaria', '2024');

-- Verificar tablas creadas
SHOW TABLES;

-- Verificar estructura de tabla cursos
DESCRIBE cursos;

-- Verificar estructura de tabla estudiantes_cursos
DESCRIBE estudiantes_cursos;
