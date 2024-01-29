from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # declarar una vez y se llama con el punto

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username cuando muestre datos de esta tabla los va a mostrar a traves de este dato

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }


class User(db.Model):# corresponde a la base sql alquemy  linea 3
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(35), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    favorite = db.relationship("Favorites") # uniendo las dos tablas

    def __repr__(self):
                # nombre de la clase
        return '<User %r>' % self.email # se coloca algo que no se repita despues del %
    
    def serialize(self): #serialize todos los datos de la tabla menos el passowrd
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "last_name": self.last_name
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    favorite = db.relationship("Favorites")

    def __repr__(self):
                # nombre de la clase
        return '<Planet %r>' % self.name

    def serialize(self): #serialize todos los datos de la tabla menos el passowrd
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    favorite = db.relationship("Favorites") #estamos uniendo las 2 tablas 

    def __repr__(self):
                # nombre de la clase
        return '<Character %r>' % self.name

    def serialize(self): #serialize todos los datos de la tabla menos el passowrd
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }
    
class Favorites(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))

    def __repr__(self):
                # nombre de la clase
        return '<Favorites %r>' % self.id
    
    def serialize(self): #serialize todos los datos de la tabla menos el passowrd
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id
        }

#ir al archivo admin.py