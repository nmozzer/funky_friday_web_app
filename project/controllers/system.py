from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from .. import db
from ..models import System, Improvement
from sqlalchemy import asc

system = Blueprint('system', __name__)

@system.route('/systems')
def systems():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    if request.args.get('system_add'):
        flash('System Successfully Added')
    
    if request.args.get('system_edit'):
        flash('System Successfully Edited')
    
    if request.args.get('system_delete') == 'successful':
        flash('System Successfully Deleted')
    
    if request.args.get('system_delete') == 'unsuccessful':
        flash('System Unsuccessfully Deleted: User must be an admin to delete a system')
    


    all_systems = db.session.query(System).order_by(asc(System.priority))

    return render_template('systems.html', systems=all_systems)

@system.route('/systems/view')
def view():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    if request.args.get('improvement_add'):
        flash('Improvement Successfully Added')
    
    if request.args.get('improvement_edit'):
        flash('Improvement Successfully Edited')
    
    if request.args.get('improvement_delete') == 'successful':
        flash('Improvement Successfully Deleted')
    
    if request.args.get('system_delete') == 'unsuccessful':
        flash('Improvement Unsuccessfully Deleted: User must be an admin to delete a system')


    system_id = request.args.get('system_id');

    system = System.query.filter_by(id=system_id).first()
    improvements = Improvement.query.filter_by(system_id=system.id)

    return render_template('system_view.html', system=system, improvements=improvements)

@system.route('/systems/create')
def create():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    priorities = [1, 2, 3, 4, 5]
    system_health = ['Healthy', 'Needs Improvement', 'Unhealthy']
    languages = ['Perl', 'Java', 'Typescript']
    tech_stacks = ['NAWS', 'MAWS']
    return render_template('create_system.html', 
    priorities=priorities, system_health=system_health,
    languages=languages, tech_stacks=tech_stacks)

@system.route('/systems/create', methods=['POST'])
def create_post():
    if not current_user.is_authenticated:
         return redirect(url_for('auth.login'))
   

    priority = request.form.get('priority')
    health = request.form.get('system_health')
    name = request.form.get('name')
    language = request.form.get('language')
    tech_stack = request.form.get('tech_stack')
    description = request.form.get('description')

    system = System.query.filter_by(name=name).first() 

    if system: 
        flash('System already exists')
        return redirect(url_for('.create'))

    new_system = System(name=name, system_health=health, priority=priority, language=language, tech_stack=tech_stack, description=description)

    db.session.add(new_system)
    db.session.commit()
    return redirect(url_for('.systems', system_add='successful'))

@system.route('/systems/edit')
def edit():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    system_id = request.args.get('system_id');
    system = System.query.filter_by(id=system_id).first() 

    priorities = [1, 2, 3, 4, 5]
    system_health = ['Healthy', 'Needs Improvement', 'Unhealthy']
    languages = ['Perl', 'Java', 'Typescript']
    tech_stacks = ['NAWS', 'MAWS']
    return render_template('edit_system.html', 
    priorities=priorities, system_health=system_health,
    languages=languages, tech_stacks=tech_stacks, system=system)

@system.route('/systems/edit', methods=['POST'])
def edit_post():
    if not current_user.is_authenticated:
         return redirect(url_for('auth.login'))
   
    priority = request.form.get('priority')
    health = request.form.get('system_health')
    name = request.form.get('name')
    language = request.form.get('language')
    tech_stack = request.form.get('tech_stack')
    description = request.form.get('description')

    system_id = request.form.get('system_id');

    System.query.filter_by(id=system_id).update(dict(name=name, system_health=health, priority=priority, language=language, tech_stack=tech_stack, description=description))

    db.session.commit()
    return redirect(url_for('.systems', system_edit='successful', system_id=system_id))

@system.route('/systems/delete')
def delete():
    if not current_user.is_authenticated:
         return redirect(url_for('auth.login'))

    if current_user.type == 'admin':
        system_id = request.args.get('system_id');
        system = System.query.filter_by(id=system_id).first() 

        db.session.delete(system);
        db.session.commit()
        return redirect(url_for('.systems', system_delete='successful'))

    return redirect(url_for('.systems', system_delete='unsuccessful'))


