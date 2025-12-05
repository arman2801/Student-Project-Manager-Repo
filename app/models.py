from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student, supervisor, admin

    # For students: their tasks
    assigned_tasks = db.relationship(
        "Task",
        backref="student",
        lazy=True,
        foreign_keys="Task.assigned_to_id"
    )


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)

    assigned_by_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    assigned_by_role = db.Column(db.String(20))  # admin or supervisor

    assigned_to_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    due_date = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default="Pending")  # Pending, Submitted, Reviewed

    submission_text = db.Column(db.Text)
    submission_file = db.Column(db.String(255))  # file path

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
