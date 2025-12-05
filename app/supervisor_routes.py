from flask import Blueprint, render_template, redirect, url_for, session, current_app, send_from_directory
from .security import login_required
from .models import User, Task
from .forms import TaskAssignForm, TaskEditForm
from . import db

supervisor_bp = Blueprint("supervisor", __name__, url_prefix="/supervisor")


@supervisor_bp.route("/dashboard")
@login_required(roles="supervisor")
def dashboard():
    students = User.query.filter_by(role="student").all()
    tasks = Task.query.all()
    return render_template("dashboard_supervisor.html", students=students, tasks=tasks)


@supervisor_bp.route("/task/create/<int:student_id>", methods=["GET", "POST"])
@login_required(roles="supervisor")
def create_task(student_id):
    student = User.query.get_or_404(student_id)
    if student.role != "student":
        return "Cannot assign tasks to non-student", 400

    form = TaskAssignForm()
    form.student.choices = [(student.id, student.fullname)]

    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            assigned_by_id=session["user_id"],
            assigned_by_role="supervisor",
            assigned_to_id=form.student.data,
            due_date=form.due_date.data,
            status="Pending"
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("supervisor.dashboard"))

    return render_template("tasks/create.html", form=form, from_role="supervisor")


@supervisor_bp.route("/task/edit/<int:task_id>", methods=["GET", "POST"])
@login_required(roles="supervisor")
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskEditForm(obj=task)

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.status = form.status.data
        db.session.commit()
        return redirect(url_for("supervisor.dashboard"))

    return render_template("tasks/edit.html", form=form, task=task, from_role="supervisor")


@supervisor_bp.route("/task/delete/<int:task_id>")
@login_required(roles="supervisor")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("supervisor.dashboard"))


@supervisor_bp.route("/task/<int:task_id>/view")
@login_required(roles="supervisor")
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template("tasks/view.html", task=task, from_role="supervisor")


@supervisor_bp.route("/uploads/<filename>")
@login_required(roles="supervisor")
def download_file(filename):
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(upload_folder, filename, as_attachment=True)
