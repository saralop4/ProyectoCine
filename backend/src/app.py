from flask import Flask

from routes.user import user
from routes.admin import admin
from routes.superadmin import superadmin
from routes.peliculas import movie

app = Flask(__name__)

# ---------------------------------------------------------------------------- #
#                                 USUARIO FINAL                                #
# ---------------------------------------------------------------------------- #

app.register_blueprint(user)
app.register_blueprint(admin)
app.register_blueprint(superadmin)
app.register_blueprint(movie)


if __name__ == '__name__':
    app.run(port=4000, debug=True)