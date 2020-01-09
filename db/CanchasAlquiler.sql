CREATE DATABASE IF NOT EXISTS `CanchasAlquiler`;

CREATE TABLE `Usuario` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(60) NOT NULL,
  `clave` VARCHAR(100) NOT NULL,
  `correo` VARCHAR(100) NOT NULL,
  `apodo` VARCHAR(50) NOT NULL,
  `tipo_usuario` TINYINT NOT NULL,
  `telefono` VARCHAR(100) NULL,
  `numero_reservas` INT UNSIGNED NULL,
  PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Equipo` (
  `id`                INT unsigned NOT NULL AUTO_INCREMENT,
  `capitan`           INT unsigned NOT NULL REFERENCES `Usuario`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  `apodo`             VARCHAR(30) NOT NULL, /*pueden existir dobles*/
  `cantidad_miembros` INT UNSIGNED NOT NULL,
  `foto_equipo`       TEXT NOT NULL,
  PRIMARY KEY(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

/* ciudad no la puse, podríamos hacer otra tabla y que el lugar esté contenido 
en esa, que a su vez ciudad tenga uno que se llame provincia, algo así. */
CREATE TABLE `Lugar` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `owner` VARCHAR(60) NOT NULL,
  `nombre` VARCHAR(50) NOT NULL,
  `anunciada` TINYINT UNSIGNED NULL,
  `bar`    TINYINT UNSIGNED NULL,
  `preciodia` INT UNSIGNED NOT NULL,
  `precionoche` INT UNSIGNED NOT NULL,
  `incluye` VARCHAR(250) NOT NULL,
  `fotoperfil` TEXT NOT NULL,
  `fotoportada` TEXT NOT NULL,
  `estacionamiento` TINYINT UNSIGNED NULL,
  `parrilla` TINYINT UNSIGNED NULL, 
  `ciudad` VARCHAR(100) NOT NULL,
  `telefono` VARCHAR(100) NOT NULL,
  `correo_owner` VARCHAR(100) NOT NULL,
  `provincia` VARCHAR(100) NOT NULL,
  `total_likes` INT UNSIGNED NULL,
  PRIMARY KEY(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Cancha` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_lugar` INT UNSIGNED NOT NULL REFERENCES `Lugar`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  `tipo_de_pasto` VARCHAR(100) NOT NULL,
  `tipo_de_piso` VARCHAR(100) NOT NULL, 
  `techado` TINYINT UNSIGNED NULL,
  `iluminacion` TINYINT UNSIGNED NULL,
  `fotodecancha` TEXT,
  PRIMARY KEY(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;


/********* CARACTERÍSTICAS DE LA CANCHA **********/

/* 
You could store it as an integer of the number of minutes past midnight:
eg.

0 = 00:00 
60 = 01:00
252 = 04:12

from datetime import timedelta
hora_int = 252
hora = 0
if hora >= 60:
  hora_int-=60
  hora+=1
timedelta(hours=hora, minutes=hora_int)


You would however need to write some code to reconstitute the time, but that shouldn't be tricky.
 */

CREATE TABLE `HorarioNormal` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_lugar` INT UNSIGNED NOT NULL REFERENCES `Lugar`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  `diadelasemana` SMALLINT UNSIGNED NULL, /* 0-6 */
  `horadeapertura_dia` INT NULL,
  `horadecierre_dia` INT NULL,
  `horadeapertura_tarde` INT NULL,
  `horadecierre_tarde` INT NULL,
  `vacaciones` TINYINT UNSIGNED NULL,
  PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `HorarioAnulado` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_lugar` INT UNSIGNED NOT NULL REFERENCES `Lugar`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  `fechadeanulacioncomienzo`  DATETIME,
  `fechadeanulacionfinal`     DATETIME,
  `diadelaSemana`             INT UNSIGNED NULL,
  `horamodificadadeapertura`  INT,
  `horamodificadadacierre`    INT,
  `cerradohoy`                TINYINT,
  PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*
  To find open shops is trivial, but you also need to check if there are override hours:

  SELECT Shop
  FROM OverrideHours
  WHERE OverrideStartDate <= NOW()
  AND OverrideEndDate >= NOW()
  AND DayOfWeek = WEEKDAY(NOW())

  If there are any record returned, those shops have alternate hours or are closed.
*/

CREATE TABLE `Deportes` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tipo_deporte` VARCHAR(50) NOT NULL,
  `id_lugar` INT UNSIGNED REFERENCES `Lugar`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

/****** ACCIONES DEL USUARIO ******/
CREATE TABLE `AlquilaLugar` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_persona_alquila` INT UNSIGNED NOT NULL REFERENCES `Usuario`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  `id_lugar` INT UNSIGNED NOT NULL REFERENCES `Lugar`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  `fecha_peticion_realizada` DATETIME,
  `diadelasemana` SMALLINT UNSIGNED NULL, /* 0-6 */
  `fechaalquiler` DATE,
  `horacomienzo` SMALLINT UNSIGNED NULL,
  `senado` INT UNSIGNED NOT NULL,
  `tiempo` INT UNSIGNED NOT NULL,
  `confirmado` TINYINT UNSIGNED NULL
  PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `PoseeEquipo` (
  `id_persona` INT UNSIGNED NOT NULL REFERENCES `Usuario`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  `id_equipo` INT UNSIGNED NOT NULL REFERENCES `Equipo`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  PRIMARY KEY (`id_persona`, `id_equipo`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `Denuncias` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT, 
  `id_persona` INT UNSIGNED NOT NULL REFERENCES `Usuario`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  `id_lugar` INT UNSIGNED NOT NULL REFERENCES `Lugar`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `LeGusta` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT, 
  `id_persona` INT UNSIGNED NOT NULL REFERENCES `Usuario`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  `id_lugar` INT UNSIGNED NOT NULL REFERENCES `Lugar`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `revoked_tokens` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `jti` VARCHAR(120) NOT NULL,
  PRIMARY KEY (`id`)
);
