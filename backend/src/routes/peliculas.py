from flask import Blueprint, jsonify, make_response, request
from sqlite3 import Error
from util.connect import create_connection

movie = Blueprint('movie', __name__, url_prefix='/movie')

@movie.route('/<title>', methods=['GET'])
def searchMovie(title):
    conn = create_connection()
    with conn:
        try:
            sql = "SELECT * FROM Peliculas WHERE titulo LIKE '%{}%'".format(title)   

            cursor = conn.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()

            body = []

            for fila in filas:
                pelicula = {
                    'idPelicula': fila[0],
                    'titulo': fila[3],
                    'sinopsis': fila[4],
                    'genero': fila[5],
                    'fechaEstreno': fila[6],
                    'duracion': fila[7],
                    'disponibilidad': fila[8],
                    'clasificacion': fila[9],
                    'pais': fila[10],
                    'tipoFormato': fila[11],
                }
                body.append(pelicula)

            return make_response(jsonify({'error': False, 'body': body}), 201)

        except Error as e:    
            response={
                'error': True,
                "message": e
            }

            return make_response(jsonify(response), 404)
        finally:
            conn.commit()

@movie.route('/actives', methods=['GET'])
def searchActivesMovies():
    conn = create_connection()
    with conn:
        try:
            sql = "SELECT idPelicula, titulo, sinopsis, genero, fechaEstreno, duracion, clasificacion, pais, tipoFormato FROM Peliculas WHERE tipoDisponibilidad = 'Activo'"   

            cursor = conn.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()

            body = []

            for fila in filas:
                pelicula = {
                    'idPelicula': fila[0],
                    'titulo': fila[1],
                    'sinopsis': fila[2],
                    'genero': fila[3],
                    'fechaEstreno': fila[4],
                    'duracion': fila[5],
                    'clasificacion': fila[6],
                    'pais': fila[7],
                    'tipoFormato': fila[8],
                }
                body.append(pelicula)

            return make_response(jsonify({'error': False, 'body': body}), 201)

        except Error as e:    
            response={
                'error': True,
                "message": e
            }

            return make_response(jsonify(response), 404)
        finally:
            conn.commit()

@movie.route('/save', methods=['POST'])
def saveMovie():
    conn = create_connection()
    with conn:
        try:
            idUser = request.json['idUser']
            titulo = request.json['titulo']
            sinopsis = request.json['sinopsis']
            genero = request.json['genero']
            fechaEstreno = request.json['fechaEstreno']
            duracion = request.json['duracion']
            tipoDisponibilidad = request.json['tipoDisponibilidad']
            clasificacion = request.json['clasificacion']
            pais = request.json['pais']
            tipoFormato = request.json['tipoFormato']
           
            if 'Admin' in idUser:
                sql = "INSERT INTO Peliculas(idAdministrador, titulo, sinopsis, genero, fechaEstreno, duracion, tipoDisponibilidad, clasificacion, pais, tipoFormato) VALUES (?,?,?,?,?,?,?,?,?,?)"   
            else:
                sql = "INSERT INTO Peliculas(idSuperAdmin, titulo, sinopsis, genero, fechaEstreno, duracion, tipoDisponibilidad, clasificacion, pais, tipoFormato) VALUES (?,?,?,?,?,?,?,?,?,?)"
                
            data = (idUser, titulo, sinopsis, genero, fechaEstreno, duracion, tipoDisponibilidad, clasificacion, pais, tipoFormato)

            conn.execute(sql, data)

            response={
                        'error': False,
                        "message": 'La pelicula ha sido guardada'
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

@movie.route('/delete', methods=['DELETE'])
def deleteMovie():
    conn = create_connection()
    with conn:
        try:
            idPelicula = request.json['idPelicula']
            titulo = request.json['titulo']
            clasificacion = request.json['clasificacion']
            pais = request.json['pais']
            
                      
            sql = "DELETE FROM Peliculas WHERE idPelicula = ? AND titulo = ? AND clasificacion = ? AND pais = ?"
            data = (idPelicula, titulo, clasificacion, pais)

            conn.execute(sql, data)

            response={
                        'error': False,
                        "message": 'La pelicula {} ha sido eliminada'.format(titulo)
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

@movie.route('/update', methods=['PUT'])
def updateMovie():
    conn = create_connection()
    with conn:
        try:

            clasificacion = request.json["clasificacion"]
            disponibilidad = request.json["disponibilidad"]
            duracion = request.json["duracion"]
            fechaEstreno = request.json["fechaEstreno"]
            genero = request.json["genero"]
            idPelicula = request.json["idPelicula"]
            pais = request.json["pais"]
            sinopsis = request.json["sinopsis"]
            tipoFormato = request.json["tipoFormato"]
            titulo = request.json["titulo"]
                      
            sql = "UPDATE Peliculas SET clasificacion = ?, tipoDisponibilidad = ?, duracion = ?, fechaEstreno = ?, genero = ?, pais = ?, sinopsis = ?, tipoFormato = ?, titulo = ? WHERE idPelicula = ?"
            data = (clasificacion, disponibilidad, duracion, fechaEstreno, genero, pais, sinopsis, tipoFormato, titulo, idPelicula)

            conn.execute(sql, data)

            response={
                        'error': False,
                        "message": 'La pelicula {} ha sido actualizada.'.format(titulo)
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