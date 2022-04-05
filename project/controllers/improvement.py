from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from .. import db
from ..models import System, Improvement
from sqlalchemy import desc

improvement = Blueprint('improvement', __name__)

@improvement.route('/improvements')
def improvements():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    all_improvements = db.session.query(Improvement).order_by(desc(Improvement.created_at))

    return render_template('improvements.html', improvements=all_improvements)

@improvement.route('/improvements/view')
def view():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    improvement_id = request.args.get('improvement_id')
    system_id = request.args.get('system_id')
    came_from = request.args.get('came_from')

    improvement = Improvement.query.filter_by(id=improvement_id).first()
    system = System.query.filter_by(id=system_id)

    return render_template('improvement_view.html', improvement=improvement, system=system, came_from=came_from)

@improvement.route('/improvements/create')
def create():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    system_id = request.args.get('system_id')
    system = System.query.filter_by(id=system_id)

    return render_template('create_improvement.html', system=system)

@improvement.route('/improvements/create', methods=['POST'])
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

@improvement.route('/improvements/edit')
def edit():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    improvement_id = request.args.get('improvement_id');
    improvement = Improvement.query.filter_by(id=improvement_id).first() 

 
    return render_template('edit_improvement.html', improvement=improvement)

@improvement.route('/improvements/edit', methods=['POST'])
def edit_post():
    if not current_user.is_authenticated:
         return redirect(url_for('auth.login'))

    name = request.form.get('name')
    description = request.form.get('description')
    beans = request.form.get('beans')
    system_id = request.form.get('system_id')
    improvement_id = request.form.get('improvement_id');

    Improvement.query.filter_by(id=improvement_id).update(dict(name=name, description=description, beans=beans))

    db.session.commit()
    return redirect(url_for('system.view', improvement_edit='successful'), system_id=system_id)

@improvement.route('/improvements/delete')
def delete():
    if not current_user.is_authenticated:
         return redirect(url_for('auth.login'))
    
    improvement_id = request.args.get('improvement_id');
    system_id = request.args.get('system_id')

    if current_user.type == 'admin':
        improvement = Improvement.query.filter_by(id=improvement_id).first() 

        db.session.delete(improvement);
        db.session.commit()
        return redirect(url_for('system.view', improvement_delete='successful'), system_id=system_id)
    
    return redirect(url_for('system.view', improvement_delete='unsuccessful'), system_id=system_id)


