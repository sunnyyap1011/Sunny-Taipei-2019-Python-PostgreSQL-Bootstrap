import peeweedbevolve
import peewee as pw
from flask import Flask, flash, render_template, request, redirect, url_for
from models import db, Store, Warehouse
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

@app.route("/stores/new")
def stores_new():
    stores = Store.select()
    return render_template('stores_new.html', stores=stores)
    

@app.route("/stores", methods=["POST"])
def stores_create():
    s = Store(name=request.form['store_name'])

    try:
        if s.save():
            flash(f'{s.name} successfully added', 'success')
            return redirect(url_for('stores_new'))

    except pw.IntegrityError:
        flash(f'{s.name} already exists', 'danger')
        return redirect(url_for('stores_new'))


@app.route("/stores")
def stores_index():
    stores = Store.select()
    return render_template('stores.html', stores=stores)


@app.route("/stores/<store_id>")
def stores_show(store_id):
    store = Store.get_by_id(store_id)
    return render_template('stores_show.html', store=store, store_id=store_id)


@app.route("/stores/<store_id>", methods=['POST'])
def stores_update(store_id):
    s = Store.get_by_id(store_id)
    s.name = request.form['store_name']

    try:
        if s.save():
            flash(f'{s.name} successfully updated', 'success')
            return redirect(url_for('stores_show', store_id=store_id))

    except:
        flash('Please try again', 'danger')
        return redirect(url_for('stores_show', store_id=store_id))


@app.route("/stores/<store_id>/delete", methods=['POST'])
def stores_destroy(store_id):
    s = Store.get_by_id(store_id)

    try:
        if s.delete_instance():
            flash('Successfully deleted', 'success')
            return redirect(url_for('stores_index'))

    except:
        flash('Please try again', 'danger')
        return redirect(url_for('stores_index'))


@app.route("/warehouses/new")
def warehouses_new():
    warehouses = Warehouse.select()
    stores = Store.select()
    return render_template('warehouse.html', warehouses=warehouses , stores=stores)


@app.route("/warehouses", methods=["POST"])
def warehouses_create():

    try:
        store = Store.get_by_id(request.form['store_id'])
        w = Warehouse(location=request.form['location'], store=store)
        if w.save():
            flash(f'{w.location} successfully added', 'success')
            return redirect(url_for('warehouses_new'))

    except pw.IntegrityError:
        flash(f'{store.name} already assigned a warehouse', 'danger')
        return redirect(url_for('warehouses_new'))
    
    except:
        flash('Please try again', 'danger')
        return redirect(url_for('warehouses_new'))


if __name__ == '__main__':
    app.run()