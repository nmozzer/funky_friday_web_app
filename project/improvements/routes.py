from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask import current_app as app
from flask_login import current_user, login_required
from .. import db
from ..models import System, Improvement
from sqlalchemy import desc

improvement = Blueprint('improvement', __name__, template_folder='templates', static_folder='static')

@improvement.errorhandler(500)
def internal_error(error):
    return render_template('500.html', error=error), 500

@improvement.route('/improvements')
@login_required
def improvements():
    all_improvements = db.session.query(Improvement).order_by(desc(Improvement.created_at))
    try:
        return render_template('improvements.html', improvements=all_improvements)
    except Exception as e:
        abort(500)

@improvement.route('/improvements/view')
@login_required
def view():
    improvement_id = request.args.get('improvement_id')
    system_id = request.args.get('system_id')
    came_from = request.args.get('came_from')

    improvement = Improvement.query.filter_by(id=improvement_id).first()
    system = System.query.filter_by(id=system_id)
    
    try:
        return render_template('improvement_view.html', improvement=improvement, system=system, came_from=came_from)
    except Exception as e:
        abort(500)

@improvement.route('/improvements/create')
@login_required
def create():   
    system_id = request.args.get('system_id')
    print(system_id)
    system = System.query.filter_by(id=system_id).first()

    try:
        return render_template('create_improvement.html', system=system)
    except Exception as e:
        abort(500)

@improvement.route('/improvements/create', methods=['POST'])
@login_required
def create_post():  
    name = request.form.get('name')
    description = request.form.get('description')
    beans = request.form.get('beans')
    system_id = request.form.get('system_id')

    improvements = Improvement.query.filter_by(system_id=system_id)

    for improvement in improvements:
        if improvement.name == name: 
            flash('Improvement already exists')
            return redirect(url_for('.create'))

    print(system_id)
    new_improvement = Improvement(name=name, description=description, beans=beans, system_id=system_id, user_id=current_user.id)

    db.session.add(new_improvement)
    db.session.commit()

    try:
        return redirect(url_for('system.view', system_id=system_id, improvement_add='successful'))
    except Exception as e:
        abort(500)

@improvement.route('/improvements/edit')
@login_required
def edit():
    improvement_id = request.args.get('improvement_id');
    improvement = Improvement.query.filter_by(id=improvement_id).first() 
    system_id = request.args.get('system_id')

    try:
        return render_template('edit_improvement.html', improvement=improvement, system_id=system_id)
    except Exception as e:
        abort(500)

@improvement.route('/improvements/edit', methods=['POST'])
@login_required
def edit_post():
    name = request.form.get('name')
    description = request.form.get('description')
    beans = request.form.get('beans')
    improvement_id = request.form.get('improvement_id');
    system_id = request.form.get('system_id')

    Improvement.query.filter_by(id=improvement_id).update(dict(name=name, description=description, beans=beans, user_id=current_user.id))

    db.session.commit()

    try:
        return redirect(url_for('system.view', improvement_edit='successful', system_id=system_id))
    except Exception as e:
        abort(500)

@improvement.route('/improvements/delete')
@login_required
def delete(): 
    improvement_id = request.args.get('improvement_id');
    system_id = request.args.get('system_id')

    if current_user.type == 'admin':
        improvement = Improvement.query.filter_by(id=improvement_id).first() 

        db.session.delete(improvement);
        db.session.commit()
        return redirect(url_for('system.view', improvement_delete='successful', system_id=system_id))

    try:
        return redirect(url_for('system.view', improvement_delete='unsuccessful', system_id=system_id))
    except Exception as e:
        abort(500)


