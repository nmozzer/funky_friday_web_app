from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .. import db
from ..models import System
from sqlalchemy import asc

system = Blueprint('system', __name__)


@system.route('/system')
def system():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    all_systems = db.session.query(System).order_by(asc(System.priority))

    return render_template('system.html', systems=all_systems)

@system.route('/system/create_system')
def create_system():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    if request.args.get('system_add') == True:
        flash('System Successfully Added')

    priorities = [1, 2, 3, 4, 5]
    system_health = ['Healthy', 'Needs Improvement', 'Unhealthy']
    languages = ['Perl', 'Java', 'Typescript']
    tech_stacks = ['NAWS', 'MAWS']
    return render_template('create_system.html', 
    priorities=priorities, system_health=system_health,
    languages=languages, tech_stacks=tech_stacks)

@system.route('/system/create_system', methods=['POST'])
def create_system_post():
    if not current_user.is_authenticated:
         return redirect(url_for('auth.login'))
   

    priority = request.form.get('priority')
    health = request.form.get('system_health')
    name = request.form.get('name')
    language = request.form.get('language')
    tech_stack = request.form.get('tech_stack')
    description = request.form.get('description')

    system = System.query.filter_by(name=name).first() # if this returns a name, then the System already exists in database

    if system: 
        flash('System already exists')
        return redirect('.create_system')

    new_system = System(name=name, system_health=health, priority=priority, language=language, tech_stack=tech_stack, description=description)

    db.session.add(new_system)
    db.session.commit()
    return redirect(url_for('.system', system_add=True))
