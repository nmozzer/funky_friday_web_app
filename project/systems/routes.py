from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask import current_app as app
from flask_login import current_user, login_required
from .. import db
from ..models import System, Improvement
from sqlalchemy import asc

system = Blueprint(
    "system", __name__, template_folder="templates", static_folder="static"
)


@system.errorhandler(500)
def internal_error(error):
    return render_template("500.html", error=error), 500


@system.route("/systems")
@login_required
def systems():
    if request.args.get("system_add"):
        flash("System Successfully Added")

    if request.args.get("system_edit"):
        flash("System Successfully Edited")

    if request.args.get("system_delete") == "successful":
        flash("System Successfully Deleted")

    if request.args.get("system_delete") == "unsuccessful":
        flash("System Unsuccessfully Deleted: User must be an admin to delete a system")

    all_systems = db.session.query(System).order_by(asc(System.priority))
    try:
        return render_template("systems.html", systems=all_systems)
    except Exception as e:
        abort(500)


@system.route("/systems/view")
@login_required
def view():
    if request.args.get("improvement_add"):
        flash("Improvement Successfully Added")

    if request.args.get("improvement_edit"):
        flash("Improvement Successfully Edited")

    if request.args.get("improvement_delete") == "successful":
        flash("Improvement Successfully Deleted")

    if request.args.get("system_delete") == "unsuccessful":
        flash(
            "Improvement Unsuccessfully Deleted: User must be an admin to delete a system"
        )

    system_id = request.args.get("system_id")

    system = System.query.filter_by(id=system_id).first()
    improvements = Improvement.query.filter_by(system_id=system_id).all()

    try:
        return render_template(
            "system_view.html", system=system, improvements=improvements
        )
    except Exception as e:
        abort(500)


@system.route("/systems/create")
@login_required
def create():
    priorities = [1, 2, 3, 4, 5]
    system_health = ["Healthy", "Needs Improvement", "Unhealthy"]
    languages = ["Perl", "Java", "Typescript"]
    tech_stacks = ["NAWS", "MAWS"]

    try:
        return render_template(
            "create_system.html",
            priorities=priorities,
            system_health=system_health,
            languages=languages,
            tech_stacks=tech_stacks,
        )
    except Exception as e:
        abort(500)


@system.route("/systems/create", methods=["POST"])
@login_required
def create_post():
    priority = request.form.get("priority")
    health = request.form.get("system_health")
    name = request.form.get("name")
    language = request.form.get("language")
    tech_stack = request.form.get("tech_stack")
    description = request.form.get("description")

    system = System.query.filter_by(name=name).first()

    if system:
        flash("System already exists")
        return redirect(url_for(".create"))

    new_system = System(
        name=name,
        system_health=health,
        priority=priority,
        language=language,
        tech_stack=tech_stack,
        description=description,
    )

    db.session.add(new_system)
    db.session.commit()
    try:
        return redirect(url_for(".systems", system_add="successful"))
    except Exception as e:
        abort(500)


@system.route("/systems/edit")
@login_required
def edit():
    system_id = request.args.get("system_id")
    system = System.query.filter_by(id=system_id).first()

    priorities = [1, 2, 3, 4, 5]
    system_health = ["Healthy", "Needs Improvement", "Unhealthy"]
    languages = ["Perl", "Java", "Typescript"]
    tech_stacks = ["NAWS", "MAWS"]
    try:
        return render_template(
            "edit_system.html",
            priorities=priorities,
            system_health=system_health,
            languages=languages,
            tech_stacks=tech_stacks,
            system=system,
        )
    except Exception as e:
        abort(500)


@system.route("/systems/edit", methods=["POST"])
@login_required
def edit_post():
    priority = request.form.get("priority")
    health = request.form.get("system_health")
    name = request.form.get("name")
    language = request.form.get("language")
    tech_stack = request.form.get("tech_stack")
    description = request.form.get("description")

    system_id = request.form.get("system_id")

    System.query.filter_by(id=system_id).update(
        dict(
            name=name,
            system_health=health,
            priority=priority,
            language=language,
            tech_stack=tech_stack,
            description=description,
        )
    )

    db.session.commit()
    try:
        return redirect(
            url_for(".systems", system_edit="successful", system_id=system_id)
        )
    except Exception as e:
        abort(500)


@system.route("/systems/delete")
@login_required
def delete():
    if current_user.type == "admin":
        system_id = request.args.get("system_id")
        system = System.query.filter_by(id=system_id).first()

        db.session.delete(system)
        db.session.commit()
        try:
            return redirect(url_for(".systems", system_delete="successful"))
        except Exception as e:
            abort(500)

        try:
            return redirect(url_for(".systems", system_delete="unsuccessful"))
        except Exception as e:
            abort(500)
