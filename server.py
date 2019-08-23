import peeweedbevolve
import peewee as pw
from flask import Flask, flash, render_template, request, redirect, url_for
from models import db, Store
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

@app.cli.command()
def migrate():
    db.evolve(ignore_tables={'base_model'})

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/store")
def store():
    stores = Store.select()
    return render_template('store.html', stores=stores)

@app.route("/store_form", methods=["POST"])
def create():
    # Haven't git add . & git commit yet

    s = Store(name=request.form['store_name'])

    try:
        if s.save():
            flash(f'{s.name} successfully added', 'success')
            return redirect(url_for('store'))

    except:
        flash(f'{s.name} already exists', 'danger')
        return redirect(url_for('store'))


    #  Code below from 'Redirect vs Render' page

    # s = Store(name=request.form['store_name'])

    # if s.save():
    #         flash(f'{s.name} successfully added', 'success')
    #         return redirect(url_for('store'))
    
    # else:
    #     return render_template('store.html', name=request.form['store_name'])


if __name__ == '__main__':
    app.run()