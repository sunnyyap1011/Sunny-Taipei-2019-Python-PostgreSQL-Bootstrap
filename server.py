import peeweedbevolve
import peewee as pw
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from models import db, Restaurant
import os
import config

app = Flask(__name__)
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

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
                               'favicon.ico', mimetype='image/apng')

# @app.after_request
# def after_request(response):
#     db.close()
#     return response

# @app.cli.command()
# def migrate():
#     db.evolve(ignore_tables={'base_model'})

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/restaurants/new")
def restaurants_new():
    restaurants = Restaurant.select()
    return render_template('restaurants_new.html', restaurants=restaurants)
    

@app.route("/restaurants", methods=["POST"])
def restaurants_create():
    r = Restaurant(name=request.form['restaurant_name'], address=request.form['restaurant_address'], google_map_link=request.form['restaurant_google_map_link'], area_code=request.form['restaurant_area_code'])

    if r.save():
        flash(f'{r.name} successfully added', 'success')
        return redirect(url_for('restaurants_new'))

    else:
        flash(f'{r.errors[0]}', 'danger')
        return redirect(url_for('restaurants_new'))
        # return render_template('restaurants_new.html', errors=s.errors)


@app.route("/restaurants")
def restaurants_index():
    restaurants = Restaurant.select().order_by(Restaurant.area_code.asc())
    return render_template('restaurants.html', restaurants=restaurants)


@app.route("/restaurants/<restaurant_id>")
def restaurants_show(restaurant_id):
    restaurant = Restaurant.get_by_id(restaurant_id)
    return render_template('restaurants_show.html', restaurant=restaurant, restaurant_id=restaurant_id)


@app.route("/restaurants/<restaurant_id>", methods=['POST'])
def restaurants_update(restaurant_id):
    r = Restaurant.get_by_id(restaurant_id)
    # r.name = request.form['restaurant_name']

    if r:
        r.must_try = request.form['restaurant_must_try']

        try:
            if r.save():
                flash(f"{r.name}'s Must Try successfully updated", 'success')
                return redirect(url_for('restaurants_show', restaurant_id=restaurant_id))

        except:
            flash('Please try again', 'danger')
            return redirect(url_for('restaurants_show', restaurant_id=restaurant_id))

    else:
        flash('Something wrong', 'danger')
        return redirect(url_for('restaurants_show', restaurant_id=restaurant_id))


@app.route("/restaurants/<restaurant_id>/delete", methods=['POST'])
def restaurants_destroy(restaurant_id):
    r = Restaurant.get_by_id(restaurant_id)

    try:
        if r.delete_instance():
            flash('Successfully deleted', 'success')
            return redirect(url_for('restaurants_index'))

    except:
        flash('Please try again', 'danger')
        return redirect(url_for('restaurants_index'))


@app.route("/restaurants/search", methods=['POST'])
def restaurants_search():
    x = request.form['search_input']

    restaurants = Restaurant.select().where(Restaurant.name.contains(x))

    if restaurants: 
        return render_template('restaurants_search.html', restaurants=restaurants)
    else:
        flash('Sorry, NO restaurant match your search. Below are the list of restaurants available.', 'danger')
        return redirect(url_for('restaurants_index'))


# @app.route("/warehouses")
# def warehouses_index():
#     warehouses = Warehouse.select()
#     return render_template('warehouses.html', warehouses=warehouses)


# @app.route("/warehouses/new")
# def warehouses_new():
#     warehouses = Warehouse.select()
#     stores = Store.select()
#     return render_template('warehouses_new.html', warehouses=warehouses , stores=stores)


# @app.route("/warehouses", methods=["POST"])
# def warehouses_create():

#     store = Store.get_by_id(request.form['store_id'])
#     w = Warehouse(location=request.form['location'], store=store)
#     if w.save():
#         flash(f'{w.location} successfully added', 'success')
#         return redirect(url_for('warehouses_new'))

#     else:
#         flash(f'{w.errors[0]}', 'danger')
#         return redirect(url_for('warehouses_new'))


if __name__ == '__main__':
    app.run()