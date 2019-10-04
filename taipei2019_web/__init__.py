from app import app
from flask import render_template, send_from_directory
from taipei2019_web.blueprints.restaurants.views import restaurants_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
import os

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(restaurants_blueprint, url_prefix="/restaurants")


@app.route("/")
def index():
    return render_template('index.html')


# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static', 'image'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'image'),
                               'favicon.ico', mimetype='image/x-icon')
