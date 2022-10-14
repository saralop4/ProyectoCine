from sqlite3 import Connection, ProgrammingError
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, correo, password, nombre = '', apellido = '', identificacion = '', genero = '', celular= '', ciudad= '') -> None:
        self.id = id,
        self.nombre = nombre
        self.apellido= apellido
        self.identifiacion= identificacion
        self.correo = correo
        self.password = password
        self.genero = genero
        self.celular = celular
        self.ciudad = ciudad

    @classmethod
    def hash_password(self, password:str):
        return generate_password_hash(str(password))

    @classmethod
    def check_password(self, hash_pass:str, password:str):
        return check_password_hash(hash_pass, password)

    def register(self, conn:Connection):
        try:
            data=(self.nombre, self.apellido, self.identifiacion, self.correo)
            response = self.canRegisterUser(conn, data, 'UsuariosFinal')

            if response == False:
                flash("El usuario ya se encuentra registrado", 'error')
                return None
            else:
                cursor = conn.cursor()
                sql = "INSERT INTO UsuariosFinal VALUES (?,?,?,?,?,?,?,?,?, datetime('now'))"
                data = (self.id,
                        self.nombre,
                        self.apellido,
                        self.identifiacion,
                        self.correo,
                        self.hash_password(self.password),
                        self.genero,
                        self.celular,
                        self.ciudad
                        )
                filas = cursor.execute(sql, data)
                filas = cursor.fetchall()
                flash('Usuario registrado exitosamente.', 'success')
                return filas
        except Exception as e:
            flash('La información ingresada es incorrecta. {}'.format(e), 'error')
            return None
            # raise Exception(e)

    def login(self, conn):
        email = self.correo
        password = self.password

        with conn:
            cursor = conn.cursor()
            sql = 'SELECT idUsuariosFinal as id, password, correo FROM UsuariosFinal WHERE correo = ?'
            cursor.execute(sql, (email,))
            row = cursor.fetchone()
            if row == None:
                flash('EL usuario no se encuentra registrado en la base de datos', 'error')
                return None
            else:
               response = User.check_password(row[1], password)
               if response == True:
                    self.id = row[0]
                    return True
               else:
                    flash('La contraseña es incorrecta. Digitela nuevamente','error')
                    return None

    @classmethod
    def canRegisterUser(self, conn: Connection, data, table_name: str):
        """ Valida si el usuario existe en la base de datos
        :param conn: Conexión a la base de datos
        :param data: datos a verificar (identificacion, nombre, apellido)
        :return: Boolean
        """
        dicQueries = {
            'UsuariosFinal':  "SELECT * FROM UsuariosFinal WHERE nombre = ? AND apellidos = ? AND identificacion = ? AND correo = ?",
            'Administradores': "SELECT * FROM Administradores WHERE nombre = ? AND correo = ?",
            'SuperAdmins': "SELECT * FROM SuperAdmins WHERE nombre = ? AND correo = ?"
        }
        
        with conn:
            try:
                cursor = conn.cursor()
                sql = str(dicQueries.get(str(table_name)))

                cursor.execute(sql, data)
                filas = cursor.fetchall()
                
                if len(filas)==0:
                    return True
                else:
                    return False
            except ProgrammingError as pe:
                print(pe)
                return False
    
    @classmethod
    def loggerUser(self, conn:Connection, id):
        try:
            cursor = conn.cursor()
            sql = "SELECT correo, nombre, apellidos FROM UsuariosFinal WHERE idUsuariosFinal = ?"
            data = (id,)
            filas = cursor.execute(sql, data)
            filas = cursor.fetchone()
            if filas == None:
                return None
            else:
                return User(filas[0], None, filas[1], filas[2])
        except Exception as e:
            flash('{}'.format(e), 'error')
            return None
            # raise Exception(e)

