import os
from flask_admin import Admin
from models import db, User, Character, Planet, Favorites #importar las tablas
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
                        #Nombre que aparece
    admin = Admin(app, name='StarWars', template_mode='bootstrap3')

    #-----------SE CONFIGURA LAS TABLAS PARA VERLO GRAFICAMENTE -------------

    #agregar las tablas de forma visual al modelo de la base de datos----------
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(Favorites, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))


    #ir al archivo app.py para importar las tablas