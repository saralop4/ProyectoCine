from sqlite3 import Connection, ProgrammingError
from cryptography.fernet import Fernet

key = bytes('g9gNDSCtach_O-XNUp6JfH8z0U5WjJKdSeWJetwBJLw=','utf-8')

def canRegisterUser(conn: Connection, data, table_name:str):
    """ Valida si el usuario existe en la base de datos
    :param conn: Conexión a la base de datos
    :param data: datos a verificar (identificacion, nombre, apellido)
    :return: Boolean
    """

    query = {
        'UsuarioFinal':  "SELECT * FROM UsuariosFinal WHERE nombre = ? AND apellidos = ? AND identificacion = ? AND correo = ?",
        'Administradores': "SELECT * FROM Administradores WHERE nombre = ? AND correo = ?",
        'SuperAdmins': "SELECT * FROM SuperAdmins WHERE nombre = ? AND correo = ?"
    }
    
    with conn:
        try:
            cursor = conn.cursor()
            sql = query.get(table_name)

            cursor.execute(sql, data)
            filas = cursor.fetchall()

            if len(filas)==0:
                return True
            else:
                return False
        except ProgrammingError as pe:
            print(pe)
            return pe


def encrypt(message:str):
    # key = Fernet.generate_key()
    fernet = Fernet(key)
    encMessage = fernet.encrypt(message.encode())
    return encMessage.decode('utf-8')


def decrypt(message:str):
    """ Desencriptar un mensaje
    :param message: Texto encriptado
    :return: Str
    """

    # key = Fernet.generate_key()
    fernet = Fernet(key)
    decMessage = fernet.decrypt(message).decode()
    return decMessage


def validateLoginData(user, password):
    if len(user) == 0:
        response = {
                'error': True,
                'message': 'El usuario y/o contraseña son incorrecto(s).'
            }
        return response

    hash_pass = bytes(user[0][0], 'utf-8')
    pass_decrypt = decrypt(hash_pass)

    if password != pass_decrypt:
        return {
            'error': True,
            'message': 'El usuario y/o contraseña son incorrecto(s).'
        }
    
    return {
        'error': False,
        'body':''
    }

def setPrefixUser(conn: Connection, prefixes:str):
     sql = {
         'Administradores':'SELECT idAdministrador FROM Administradores ORDER BY idAdministrador DESC LIMIT 1',
         'SA': 'SELECT idSuperAdmin FROM SuperAdmins ORDER BY idSuperAdmin DESC LIMIT 1'
     }

     with conn:
        try:
            cursor = conn.cursor()
            sql = sql.get(prefixes)
            cursor.execute(sql)
            filas = cursor.fetchone()

            if filas == None:
                return prefixes + '001'
            
            numbers = filas[0].split(prefixes)[1]
            consec = int(numbers)

            prefix = ''
            if consec <= 8:
                prefix = prefixes + '00' + str(consec + 1)
            if consec >= 9 and consec <= 98:
                prefix = prefixes + '0'+ str(consec + 1)
            if consec >= 99:
                prefix = prefixes + str(consec + 1)

            return prefix
            
        except ProgrammingError as pe:
            print(pe)
            return pe
