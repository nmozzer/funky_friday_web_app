from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user


main = Blueprint('main', __name__, template_folder='templates', static_folder='static')

@main.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)