from flask import Blueprint, render_template, redirect, url_for

travel_plan_blueprint = Blueprint('travel_plan',
                            __name__,
                            template_folder='templates')


@travel_plan_blueprint.route("/")
def index():
    return render_template('travel_plan/index.html')