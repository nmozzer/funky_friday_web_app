from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user


main = Blueprint("main", __name__, template_folder="templates", static_folder="static")


@main.errorhandler(500)
def internal_error(error):
    return render_template("500.html", error=error), 500


@main.route("/")
@login_required
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        abort(500)


@main.route("/profile")
@login_required
def profile():
    try:
        return render_template("profile.html", name=current_user.name)
    except Exception as e:
        abort(500)
