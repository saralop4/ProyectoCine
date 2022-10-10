import uuid
from sqlite3 import ProgrammingError, Error
from flask import Blueprint, jsonify, make_response, request

from util.connect import create_connection
from util.fn import canRegisterUser, encrypt, validateLoginData

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/getAllUsers', methods=['GET'])
def getUsers():
    conn = create_connection()
    with conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT idUsuariosFinal, nombre, apellidos, identificacion, correo, genero, celular, ciudad FROM UsuariosFinal")
            filas = cursor.fetchall()

            if len(filas)==0:
                return make_response('No existen registros', 404)

            body = []

            for fila in filas:
                pelicula = {
                    'idUsuariosFinal': fila[0],
                    'nombre': fila[1],
                    'apellidos': fila[2],
                    'identificacion': fila[3],
                    'correo': fila[4],
                    'genero': fila[5],
                    'celular': fila[6],
                    'ciudad': fila[7],
                }
                body.append(pelicula)
           
            response = {
                'error': False,
                'message': body
            }

            return make_response(jsonify(response), 200)
        except ProgrammingError as pe:
            print(pe)
            return pe
        finally:
            conn.commit()

@user.route('/register', methods=['POST'])
def registerUser():
    conn = create_connection()
    with conn:
        try:
            idUsuariosFinal = str(uuid.uuid4())
            nombre = request.json['nombre']
            apellido = request.json['apellido']
            genero = request.json['genero']
            identificacion = request.json['identificacion']
            celular = request.json['celular']
            ciudad = request.json['ciudad']
            email = request.json['email']
            password = encrypt(request.json['password'])

            dataToValidate = (nombre, apellido, identificacion, email)
            response = canRegisterUser(conn, dataToValidate, 'UsuarioFinal')
            if response == False:
                return jsonify(
                    {
                        'error': True,
                        "message": 'Usuario ya se encuentra registrado en la base de datos'
                    }
                )

            sql = "INSERT INTO UsuariosFinal VALUES (?,?,?,?,?,?,?,?,?, datetime('now'))"
            data = (idUsuariosFinal, nombre, apellido, identificacion, email, password, genero, celular, ciudad)
            conn.execute(sql, data)

            response={
                        'error': False,
                        "message": 'EL usuario ha sido creado'
                    }

            return make_response(jsonify(response), 201)

        except Error as e:    
            response={
                'error': True,
                "message": e
            }

            return make_response(jsonify(response), 404)
        finally:
            conn.commit()
            
@user.route('/login', methods=['POST'])
def userLogin():
    conn = create_connection()
    with conn:
        try:
            email = request.json['email']
            password = request.json['password']
            cursor = conn.cursor()

            sql = "SELECT password, idUsuariosFinal, nombre, apellidos, correo, celular FROM UsuariosFinal WHERE correo = ?"
            values = (email,)
            cursor.execute(sql, values)
            user = cursor.fetchall()

            response = validateLoginData(user, password)
            
            if response.get('error') == True:
                return make_response(jsonify(response), 400)

            response['body'] = {
                "nombre": user[0][2],
                "apellido": user[0][3],
                "correo": user[0][4],
                "celular": user[0][5],
                "token": encrypt(user[0][1] + ', ' +user[0][2] +  ', ' + user[0][3])
            }
           
            return make_response(jsonify(response), 200)
        except ProgrammingError as pe:
            print(pe)
            return pe
        finally:
            conn.commit()
    