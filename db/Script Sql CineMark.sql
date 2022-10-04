CREATE TABLE DBCinemark

CREATE TABLE SuperAdmins (
  idSuperAdmin INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  nombre VARCHAR(50) NOT NULL,
  apellido VARCHAR(80) NOT NULL,
  correo VARCHAR(80) NOT NULL,
  contraseña VARCHAR(80) NOT NULL
);

CREATE TABLE Tiquetes (
  idTiquetes INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  precioTiquete DOUBLE NOT NULL,
  hora TIME NOT NULL,
  sala VARCHAR(50) NOT NULL,
  asiento VARCHAR(50) NOT NULL,
  tipoFormato VARCHAR(80) NOT NULL
);

CREATE TABLE Administradores (
  idAdministrador INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  idSuperAdmin INTEGER NOT NULL,
  correo VARCHAR(80) NOT NULL,
  contraseña VARCHAR(50) NOT NULL,
  nombre VARCHAR(80) NOT NULL,
  apellido VARCHAR(80) NOT NULL,
  PRIMARY KEY(idSuperAdmin),
  FOREIGN KEY(idSuperAdmin)
    REFERENCES SuperAdmins(idSuperAdmin)
);

CREATE TABLE Funciones (
  idFuncion INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  idSuperAdmin INTEGER NOT NULL,
  idAdministrador INTEGER NOT NULL,
  Hora TIME NOT NULL,
  CantidadTiquetes INT  NOT NULL,
  SillasDisponibles VARCHAR(30) NOT NULL,
  TipoUbicacion VARCHAR(30) NOT NULL,
  FOREIGN KEY(idAdministrador,idSuperAdmin)
    REFERENCES Administradores(idAdministrador, idSuperAdmin)
);

CREATE TABLE UsuariosFinal (
  idUsuariosFinal INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  idSuperAdmin INTEGER NOT NULL,
  idAdministrador INTEGER NOT NULL,
  nombre VARCHAR(80) NOT NULL,
  apellidos VARCHAR(80) NOT NULL,
  identificacion INTEGER NOT NULL,
  tipoIdentificacion VARCHAR(80) NOT NULL,
  correo VARCHAR(80) NOT NULL,
  contraseña VARCHAR(80) NOT NULL,
  fechaNacimiento DATE NOT NULL,
  genero VARCHAR(50) NOT NULL,
  celular INTEGER NOT NULL,
  ciudad VARCHAR(50) NOT NULL,
  direccion VARCHAR(80) NOT NULL,
  FOREIGN KEY(idAdministrador,idSuperAdmin)
    REFERENCES Administradores(idAdministrador,idSuperAdmin)
);

CREATE TABLE Peliculas (
  idPelicula INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  idSuperAdmin INTEGER NOT NULL,
  idAdministrador INTEGER  NOT NULL,
  nombre VARCHAR(50) NOT NULL,
  genero VARCHAR(50) NOT NULL,
  fechaEstreno DATETIME NOT NULL,
  duracion VARCHAR(50) NOT NULL,
  tipoDisponibilidad VARCHAR(50) NOT NULL,
  clasificacion VARCHAR(50) NOT NULL,
  pais VARCHAR(50) NOT NULL,
  tipoFormato VARCHAR(50) NOT NULL,
  FOREIGN KEY(idAdministrador, idSuperAdmin)
  REFERENCES Administradores(idAdministrador, idSuperAdmin)
);

CREATE TABLE UsuariosFinal_has_Tiquetes (
  idUsuariosFinal INTEGER NOT NULL,
  idTiquetes INTEGER NOT NULL,
  PRIMARY KEY(idUsuariosFinal,idTiquetes),
  FOREIGN KEY(idUsuariosFinal)
    REFERENCES UsuariosFinal(idUsuariosFinal),
  FOREIGN KEY(idTiquetes)
    REFERENCES Tiquetes(idTiquetes)
);

CREATE TABLE Funcion_has_Pelicula (
  idFuncion INTEGER NOT NULL,
  idPelicula INTEGER NOT NULL,
  PRIMARY KEY(idFuncion, idPelicula),
  FOREIGN KEY(idFuncion)
    REFERENCES Funciones(idFuncion),
  FOREIGN KEY(idPelicula)
    REFERENCES Peliculas(idPelicula)
);

CREATE TABLE Peliculas_has_UsuariosFinal (
  idPelicula INTEGER NOT NULL,
  idUsuariosFinal INTEGER NOT NULL,
  PRIMARY KEY(idPelicula,idUsuariosFinal),
  FOREIGN KEY(idPelicula)
  REFERENCES Peliculas(idPelicula),
  FOREIGN KEY(idUsuariosFinal)
  REFERENCES UsuariosFinal(idUsuariosFinal)
);


