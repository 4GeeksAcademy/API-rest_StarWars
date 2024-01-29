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


@app.route('/characters', methods=['GET'])
def get_characters():
    #acceda a la tabla user y traiga toda la info
    todos = Character.query.all()
    if todos == []:
        #cuando esta vacio jsonify me transforma en un objeto
        return jsonify({"msg": "No hay personajes"}), 404 
                         #callback
    resultado = list(map(lambda character: character.serialize(), todos))
    return jsonify(resultado), 200


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
