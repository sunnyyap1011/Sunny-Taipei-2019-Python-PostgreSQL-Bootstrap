from flask import Blueprint, render_template, redirect, url_for, request, flash
from models.restaurant import Restaurant

restaurants_blueprint = Blueprint('restaurants',
                            __name__,
                            template_folder='templates')


@restaurants_blueprint.route("/new")
def new():
    restaurants = Restaurant.select()
    return render_template('restaurants/new.html', restaurants=restaurants)
    

@restaurants_blueprint.route("/", methods=["POST"])
def create():
    r = Restaurant(name=request.form['restaurant_name'], address=request.form['restaurant_address'], google_map_link=request.form['restaurant_google_map_link'], area_code=request.form['restaurant_area_code'])

    if r.save():
        flash(f'{r.name} successfully added', 'success')
        return redirect(url_for('restaurants.new'))

    else:
        flash(f'{r.errors[0]}', 'danger')
        return redirect(url_for('restaurants.new'))
        # return render_template('restaurants/new.html', errors=s.errors)


@restaurants_blueprint.route("/")
def index():
    restaurants = Restaurant.select().order_by(Restaurant.area_code.asc())
    return render_template('restaurants/index.html', restaurants=restaurants)


@restaurants_blueprint.route("/<restaurant_id>")
def show(restaurant_id):
    restaurant = Restaurant.get_by_id(restaurant_id)
    return render_template('restaurants/show.html', restaurant=restaurant, restaurant_id=restaurant_id)


@restaurants_blueprint.route("/<restaurant_id>", methods=['POST'])
def update(restaurant_id):
    r = Restaurant.get_by_id(restaurant_id)
    # r.name = request.form['restaurant_name']

    if r:
        r.must_try = request.form['restaurant_must_try']
        r.notes = request.form['restaurant_notes']

        try:
            if r.save():
                flash(f"{r.name}'s Must Try successfully updated", 'success')
                return redirect(url_for('restaurants.show', restaurant_id=restaurant_id))

        except:
            flash('Please try again', 'danger')
            return redirect(url_for('restaurants.show', restaurant_id=restaurant_id))

    else:
        flash('Something wrong', 'danger')
        return redirect(url_for('restaurants.show', restaurant_id=restaurant_id))


@restaurants_blueprint.route("/<restaurant_id>/delete", methods=['POST'])
def destroy(restaurant_id):
    r = Restaurant.get_by_id(restaurant_id)

    try:
        if r.delete_instance():
            flash('Successfully deleted', 'success')
            return redirect(url_for('restaurants.index'))

    except:
        flash('Please try again', 'danger')
        return redirect(url_for('restaurants.index'))


@restaurants_blueprint.route("/search", methods=['POST'])
def search():
    x = request.form['search_input']

    restaurants = Restaurant.select().where(Restaurant.name.contains(x))

    if restaurants: 
        return render_template('restaurants/search.html', restaurants=restaurants)
    else:
        flash('Sorry, NO restaurant match your search. Below are the list of restaurants available.', 'danger')
        return redirect(url_for('restaurants.index'))
