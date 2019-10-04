from flask import Flask
from models.base_model import db
import os
import config

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'taipei2019_web')

app = Flask('TAIPEI 2019', root_path=web_dir)

app.secret_key = os.getenv('SECRET_KEY')

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()

@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
#                                'favicon.ico', mimetype='image/apng')