from flask import Blueprint, render_template, session, redirect, url_for, request, current_app, send_from_directory
from .security import login_required
from .models import Task
from .forms import SubmissionForm
from . import db
from .utils import save_uploaded_file
import os

student_bp = Blueprint("student", __name__, url_prefix="/student")


@student_bp.route("/dashboard")
@login_required(roles="student")
def dashboard():
    student_id = session["user_id"]
    tasks = Task.query.filter_by(assigned_to_id=student_id).all()
    return render_template("dashboard_student.html", tasks=tasks)


@student_bp.route("/task/<int:task_id>/submit", methods=["GET", "POST"])
@login_required(roles="student")
def submit_task(task_id):
    task = Task.query.get_or_404(task_id)

    # Security: ensure task belongs to this student
    if task.assigned_to_id != session["user_id"]:
        return "Unauthorized", 403

    form = SubmissionForm()

    if form.validate_on_submit():
        task.submission_text = form.submission_text.data

        if form.file.data:
            filename = save_uploaded_file(form.file.data)
            if filename:
                task.submission_file = filename

        task.status = "Submitted"
        db.session.commit()
        return redirect(url_for("student.dashboard"))

    # prefill existing submission
    if request.method == "GET":
        form.submission_text.data = task.submission_text

    return render_template("tasks/submit.html", form=form, task=task)


@student_bp.route("/uploads/<filename>")
@login_required(roles="student")
def download_own_file(filename):
    # Optional: student downloading own submitted file
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(upload_folder, filename, as_attachment=True)
