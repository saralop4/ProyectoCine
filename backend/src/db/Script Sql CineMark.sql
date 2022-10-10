CREATE TABLE
    UsuariosFinal (
        idUsuariosFinal VARCHAR(50) NOT NULL,
        nombre VARCHAR(80) NOT NULL,
        apellidos VARCHAR(80) NOT NULL,
        identificacion INTEGER NOT NULL,
        correo VARCHAR(80) NOT NULL UNIQUE,
        password VARCHAR(200) NOT NULL,
        genero VARCHAR(50),
        celular INTEGER NOT NULL,
        ciudad VARCHAR(50) NOT NULL,
        creado TEXT DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (idUsuariosFinal)
    );

CREATE TABLE
    Administradores (
        idAdministrador VARCHAR(10) NOT NULL,
        correo VARCHAR(80) NOT NULL UNIQUE,
        password VARCHAR(200) NOT NULL,
        nombre VARCHAR(80) NOT NULL,
        apellido VARCHAR(80) NOT NULL,
        creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(idAdministrador)
    );

CREATE TABLE
    SuperAdmins (
        idSuperAdmin VARCHAR(10) NOT NULL,
        nombre VARCHAR(50) NOT NULL,
        apellido VARCHAR(80) NOT NULL,
        correo VARCHAR(80) NOT NULL UNIQUE,
        password VARCHAR(200) NOT NULL,
        creado TEXT DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(idSuperAdmin)
    );

CREATE TABLE
    Peliculas (
        idPelicula INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        idSuperAdmin VARCHAR(10),
        idAdministrador VARCHAR(10),
        titulo VARCHAR(50) not null,
        sinopsis TEXT not null,
        genero VARCHAR(50) NOT NULL,
        fechaEstreno TEXT NOT NULL,
        duracion VARCHAR(50) NOT NULL,
        tipoDisponibilidad VARCHAR(50) NOT NULL,
        clasificacion VARCHAR(50) NOT NULL,
        pais VARCHAR(50) NOT NULL,
        tipoFormato VARCHAR(50) NOT NULL,
        FOREIGN KEY(idAdministrador, idSuperAdmin) REFERENCES Administradores(idAdministrador, idSuperAdmin)
    );

CREATE TABLE
    Tiquetes (
        idTiquetes INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        precioTiquete DOUBLE NOT NULL,
        hora TIME NOT NULL,
        sala VARCHAR(50) NOT NULL,
        asiento VARCHAR(50) NOT NULL,
        TipoUbicacion VARCHAR(30) NOT NULL
    );

CREATE TABLE
    Funciones (
        idFuncion INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        idSuperAdmin VARCHAR(10),
        idAdministrador VARCHAR(10),
        idPelicula INTEGER NOT NULL,
        Hora TIME NOT NULL,
        CantidadTiquetes INT NOT NULL,
        SillasDisponibles VARCHAR(30) NOT NULL,
        FOREIGN KEY(idAdministrador, idSuperAdmin) REFERENCES Administradores(idAdministrador, idSuperAdmin)
    );

CREATE TABLE
    UsuariosFinal_has_Tiquetes (
        idUsuariosFinal INTEGER NOT NULL,
        idTiquetes INTEGER NOT NULL,
        PRIMARY KEY(idUsuariosFinal, idTiquetes),
        FOREIGN KEY(idUsuariosFinal) REFERENCES UsuariosFinal(idUsuariosFinal),
        FOREIGN KEY(idTiquetes) REFERENCES Tiquetes(idTiquetes)
    );

CREATE TABLE
    Funcion_has_Pelicula (
        idFuncion INTEGER NOT NULL,
        idPelicula INTEGER NOT NULL,
        PRIMARY KEY(idFuncion, idPelicula),
        FOREIGN KEY(idFuncion) REFERENCES Funciones(idFuncion),
        FOREIGN KEY(idPelicula) REFERENCES Peliculas(idPelicula)
    );

CREATE TABLE
    Peliculas_has_UsuariosFinal (
        idPelicula INTEGER NOT NULL,
        idUsuariosFinal INTEGER NOT NULL,
        PRIMARY KEY(idPelicula, idUsuariosFinal),
        FOREIGN KEY(idPelicula) REFERENCES Peliculas(idPelicula),
        FOREIGN KEY(idUsuariosFinal) REFERENCES UsuariosFinal(idUsuariosFinal)
    );