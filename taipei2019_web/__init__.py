from app import app
from flask import render_template
from taipei2019_web.blueprints.restaurants.views import restaurants_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles  

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(restaurants_blueprint, url_prefix="/restaurants")


@app.route("/")
def index():
    return render_template('index.html')