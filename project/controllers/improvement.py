from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from .. import db
from ..models import System, Improvement
from sqlalchemy import desc

improvement = Blueprint('improvement', __name__)

@improvement.route('/improvement')
def improvements():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    if request.args.get('improvement_add'):
        flash('Improvement Successfully Added')
    
    if request.args.get('improvement_edit'):
        flash('Improvement Successfully Edited')
    
    if request.args.get('improvement_delete'):
        flash('Improvement Successfully Deleted')


    all_improvements = db.session.query(Improvement).order_by(desc(Improvement.created_at))

    return render_template('improvement.html', improvements=all_improvements)

@improvement.route('/improvement/view')
def view():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))


    improvement_id = request.args.get('improvement_id')
    system_id = request.args.get('system_id')


    improvement = Improvement.query.filter_by(id=improvement_id).first()
    system = System.query.filter_by(id=system_id)

    return render_template('improvement_view.html', improvement=improvement, system=system)

@improvement.route('/improvement/create')
def create():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    system_id = request.args.get('system_id')
    system = System.query.filter_by(id=system_id)


    return render_template('create_improvement.html', system=system)

@improvement.route('/improvement/create', methods=['POST'])
def create_post():
    if not current_user.is_authenticated:
         return redirect(url_for('auth.login'))
   

    name = request.form.get('name')
    description = request.form.get('description')
    beans = request.form.get('beans')
    system_id = request.form.get('system_id')

    improvements = Improvement.query.filter_by(system_id=system_id)

    for improvement in improvements:
        if improvement: 
            flash('Improvement already exists')
            return redirect(url_for('.create'))

     
    new_improvement = Improvement(name=name, description=description, beans=beans)

    db.session.add(new_improvement)
    db.session.commit()
    return redirect(url_for('system.view', improvement_add='successful'), system_id=system_id)

@improvement.route('/improvement/edit')
def edit():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    improvement_id = request.args.get('improvement_id');
    improvement = Improvement.query.filter_by(id=improvement_id).first() 

    priorities = [1, 2, 3, 4, 5]
    improvement_health = ['Healthy', 'Needs Improvement', 'Unhealthy']
    languages = ['Perl', 'Java', 'Typescript']
    tech_stacks = ['NAWS', 'MAWS']
    return render_template('edit_improvement.html', 
    priorities=priorities, improvement_health=improvement_health,
    languages=languages, tech_stacks=tech_stacks, improvement=improvement)

@improvement.route('/improvement/edit', methods=['POST'])
def edit_post():
    if not current_user.is_authenticated:
         return redirect(url_for('auth.login'))
   

    priority = request.form.get('priority')
    health = request.form.get('improvement_health')
    name = request.form.get('name')
    language = request.form.get('language')
    tech_stack = request.form.get('tech_stack')
    description = request.form.get('description')

    improvement_id = request.form.get('improvement_id');

    Improvement.query.filter_by(id=improvement_id).update(dict(name=name, improvement_health=health, priority=priority, language=language, tech_stack=tech_stack, description=description))

    db.session.commit()
    return redirect(url_for('.improvements', improvement_edit='successful', improvement_id=improvement_id))

@improvement.route('/improvement/delete')
def delete():
    if not current_user.is_authenticated:
         return redirect(url_for('auth.login'))
    
    name = current_user.__name



    improvement_id = request.args.get('improvement_id');

    improvement = Improvement.query.filter_by(id=improvement_id).first() 


    db.session.delete(improvement);
    db.session.commit()
    return redirect(url_for('.improvements', improvement_delete='successful'))


