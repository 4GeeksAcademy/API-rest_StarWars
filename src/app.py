"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorites
#from models import Person
import json

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#colocar puerto publico
@app.route('/user', methods=['GET'])
def get_usuarios():
    #acceda a la tabla user y traiga toda la info
    todos = User.query.all()
    if todos == []:
        #cuando esta vacio jsonify me transforma en un objeto
        return jsonify({"msg": "No hay usuarios"}), 404 
                         #callback
    resultado = list(map(lambda usuario: usuario.serialize(), todos))
    return jsonify(resultado), 200


@app.route('/user/favorites', methods=['GET'])
def get_usuarios_favoritos():
    body = json.loads(request.data) # traiga la info que solicito, importar despues json
        #acceda a la tabla favoritos y traiga toda la info usuario segun el id de usuario
    todos = Favorites.query.filter_by(user_id = body["user_id"]).all()
    if todos == []:
        #cuando esta vacio jsonify me transforma en un objeto
        return jsonify({"msg": "No hay favoritos para ese usuario"}), 404 
                         #callback
    resultado = list(map(lambda favorito: favorito.serialize(), todos)) # muestre por id _usuario todos los favoritos que tenga
    return jsonify(resultado), 200


@app.route('/user/<int:idUser>', methods=['GET', 'DELETE'])
def get_id_user(idUser):
    id_user = User.query.filter_by(id = idUser).first() #filtrar por el id
    if id_user is None: 
        return jsonify({"msg": "No existe el usuario"}), 404
    if request.method == "GET": 
        return jsonify(id_user.serialize()), 200 # me devulve la info, seralize me muestra la info del caracter
    if request.method == "DELETE":
        db.session.delete(id_user)
        db.session.commit()
        return jsonify({"msg": "El usuario fue eliminado"}), 200
     

@app.route('/user', methods=['POST'])
def add_user():
    body = json.loads(request.data) # traiga la info que solicito, importar despues json
            #referencia a la tabla
    nuevo_usuario = User.query.filter_by(email = body["email"]).first() #filtral a los usuario cuando email de la tabla es el mismo que ingreso en Postman
    if nuevo_usuario is None:
        nuevo_usuario = User(
            #se accede a las tablas a traves del modelo models.py
            email = body["email"],
            password = body["password"],
            name = body["name"],
            last_name = body["last_name"]
        )
        db.session.add(nuevo_usuario)#agregue 
        db.session.commit()
        return jsonify({"msg": "Usuario creado"}), 200
    return jsonify({"msg": "Ya existe el usuario"}), 404



@app.route('/characters', methods=['GET'])
def get_characters():
    #acceda a la tabla user y traiga toda la info
    todos = Character.query.all()
    if todos == []:
        #cuando esta vacio jsonify me transforma en un objeto
        return jsonify({"msg": "No hay personajes"}), 404 
                         #callback
    resultado = list(map(lambda character: character.serialize(), todos)) #devuelve array con la info
    return jsonify(resultado), 200

        #url dinamico, tipo int correspodne al id
@app.route('/characters/<int:idPersonaje>', methods=['GET', 'DELETE'])
def get_id_characters(idPersonaje):
    id_personaje = Character.query.filter_by(id = idPersonaje).first() #filtrar por el id
    if id_personaje is None: 
        return jsonify({"msg": "No existe el personaje"}), 404
    if request.method == "GET": 
        return jsonify(id_personaje.serialize()), 200 # me devulve la info, seralize me muestra la info del caracter
    if request.method == "DELETE":
        db.session.delete(id_personaje)
        db.session.commit()
        return jsonify({"msg": "El personaje fue eliminado"}), 200 

@app.route('/characters', methods=['POST'])
def add_character():
    body = json.loads(request.data) # traiga la info que solicito, importar despues json
            #referencia a la tabla
    nuevo_personaje = Character.query.filter_by(name = body["name"]).first() #filtral a los planetas cuando email de la tabla es el mismo que ingreso en Postman
    if nuevo_personaje is None: # none = no tiene nada
        nuevo_personaje = Character(
            #se accede a las tablas a traves del modelo models.py
            name = body["name"],
            description = body["description"]
        )
        db.session.add(nuevo_personaje)#agregue 
        db.session.commit() # lo graba a fuegoooo
        return jsonify({"msg": "Personaje creado"}), 200
    return jsonify({"msg": "Ya existe el personaje"}), 404



@app.route('/planets', methods=['GET'])
def get_planets():
    #acceda a la tabla user y traiga toda la info
    todos = Planet.query.all()
    if todos == []:
        #cuando esta vacio jsonify me transforma en un objeto
        return jsonify({"msg": "No hay planetas"}), 404 
                         #callback
    resultado = list(map(lambda planet: planet.serialize(), todos))
    return jsonify(resultado), 200

 #url dinamico, tipo int correspodne al id
@app.route('/planets/<int:idPlaneta>', methods=['GET', 'DELETE'])
def get_id_planets(idPlaneta):
    id_planeta = Planet.query.filter_by(id = idPlaneta).first() #filtrar por el id
    if id_planeta is None: 
        return jsonify({"msg": "No existe el planeta"}), 404
    if request.method == "GET": 
        return jsonify(id_planeta.serialize()), 200 # me devulve la info, seralize me muestra la info del caracter
    if request.method == "DELETE":
        db.session.delete(id_planeta)
        db.session.commit()
        return jsonify({"msg": "El planeta fue eliminado"}), 200 
    

@app.route('/planets', methods=['POST'])
def add_planet():
    body = json.loads(request.data) # traiga la info que solicito, importar despues json
            #referencia a la tabla
    nuevo_planeta = Planet.query.filter_by(name = body["name"]).first() #filtral a los planetas cuando email de la tabla es el mismo que ingreso en Postman
    if nuevo_planeta is None: # none = no tiene nada
        nuevo_planeta = Planet(
            #se accede a las tablas a traves del modelo models.py
            name = body["name"],
            description = body["description"]
        )
        db.session.add(nuevo_planeta)#agregue 
        db.session.commit() # lo graba a fuegoooo
        return jsonify({"msg": "Planeta creado"}), 200
    return jsonify({"msg": "Ya existe el planeta"}), 404


@app.route('/favorites', methods=['GET'])
def get_favorites():
    #acceda a la tabla user y traiga toda la info
    todos = Favorites.query.all()
    if todos == []:
        #cuando esta vacio jsonify me transforma en un objeto
        return jsonify({"msg": "No hay favoritos"}), 404 
                         #callback
    resultado = list(map(lambda favorite: favorite.serialize(), todos))
    return jsonify(resultado), 200

@app.route('/favorites', methods=['POST'])
def add_favorites():
    body = json.loads(request.data) # traiga la info que solicito, importar despues json
            #referencia a la tabla
    nuevo_favorito = Favorites(
        #se accede a las tablas a traves del modelo models.py
        user_id = body["user_id"], # a traves del body capturamos el id usuario
        planet_id = body["planet_id"],
        character_id = body["character_id"]
    )
    db.session.add(nuevo_favorito)#agregue 
    db.session.commit()
    return jsonify({"msg": "Favorito creado"}), 200


    


    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
