from flask import Blueprint, jsonify, make_response, request
from sqlite3 import Error, ProgrammingError
from util.connect import create_connection

from util.fn import canRegisterUser, encrypt, setPrefixUser, validateLoginData

superadmin = Blueprint('superadmin', __name__, url_prefix='/superadmin')

@superadmin.route('/register', methods=['POST'])
def register():
    conn = create_connection()
    with conn:
        try:
            nombre = request.json['nombre']
            apellido = request.json['apellido']
            email = request.json['email']
            password = encrypt(request.json['password'])

            dataToValidate = (nombre, email)
            response = canRegisterUser(conn, dataToValidate, 'SuperAdmins')

            userId = setPrefixUser(conn, 'SA')

            if response == False:
                return jsonify(
                    {
                        'error': True,
                        "message": 'Usuario ya se encuentra registrado en la base de datos'
                    }
                )

            sql = "INSERT INTO SuperAdmins VALUES (?,?,?,?,?, datetime('now'))"
            data = (userId, email, password, nombre, apellido)
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

@superadmin.route('/login', methods=['POST'])
def login():
    conn = create_connection()
    with conn:
        try:
            email = request.json['email']
            password = request.json['password']
            cursor = conn.cursor()

            sql = "SELECT password, idAdministrador, nombre, apellido, correo FROM Administradores WHERE correo = ?"
            values = (email,)
            cursor.execute(sql, values)
            user = cursor.fetchone()

            response = validateLoginData(user, password)
            
            if response.get('error') == True:
                return make_response(jsonify(response), 400)

            response['body'] = {
                "idAdmin": user[0][1],
                "nombre": user[0][2],
                "apellido": user[0][3],
                "correo": user[0][4],
            }
           
            return make_response(jsonify(response), 200)
        except ProgrammingError as pe:
            print(pe)
            return pe
        finally:
            conn.commit()
    