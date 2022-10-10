from flask import Blueprint, jsonify, make_response, request
from sqlite3 import Error
from util.connect import create_connection

movie = Blueprint('schedules', __name__, url_prefix='/schedule')

@movie.route('/add', methods=['POST'])
def addSchedule():
    conn = create_connection()
    with conn:
        try:
            idUser = request.json['idUser']
            idPelicula = request.json['idPelicula']
            hora = request.json['hora']
            cantidadTiquetes = request.json['cantidadTiquetes']
            sillasDisponibles = request.json['sillasDisponibles']
            tipoUbicacion = request.json['tipoUbicacion']

            if 'Admin' in idUser:
                sql = "INSERT INTO Peliculas(idAdministrador, idPelicula, hora, cantidadTiquetes, sillasDisponibles, tipoUbicacion) VALUES (?,?,?,?,?,?)" 
            else:
                sql = "INSERT INTO Peliculas(idSuperAdmin, idPelicula, hora, cantidadTiquetes, sillasDisponibles, tipoUbicacion) VALUES (?,?,?,?,?,?)"  
                
            data = (idUser, idPelicula, hora, cantidadTiquetes, sillasDisponibles, tipoUbicacion )

            conn.execute(sql, data)

            return make_response(jsonify({'error': False, 'message': 'La función ha sido agendada.'}), 201)

        except Error as e:    
            response={
                'error': True,
                "message": e
            }

            return make_response(jsonify(response), 404)
        finally:
            conn.commit()