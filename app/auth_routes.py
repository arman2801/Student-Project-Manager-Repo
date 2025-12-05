from flask import Blueprint, render_template, redirect, session, url_for
from .forms import LoginForm, RegisterForm
from .models import User
from .utils import hash_password, check_password
from . import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def index():
    return render_template("index.html")


# -----------------------
# STUDENT LOGIN
# -----------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, role="student").first()
        if user and check_password(user.password, form.password.data):
            session["user_id"] = user.id
            session["role"] = user.role
            return redirect(url_for("student.dashboard"))
        error = "Invalid student credentials"
    return render_template("login.html", form=form, error=error)


# -----------------------
# STUDENT REGISTER
# -----------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data).first()
        if existing:
            error = "Email already registered"
        else:
            hashed = hash_password(form.password.data)
            new_user = User(
                fullname=form.fullname.data,
                email=form.email.data,
                password=hashed,
                role="student"
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("auth.login"))
    return render_template("register.html", form=form, error=error)


# -----------------------
# ADMIN LOGIN
# -----------------------
@auth_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, role="admin").first()
        if user and check_password(user.password, form.password.data):
            session["user_id"] = user.id
            session["role"] = user.role
            return redirect(url_for("admin.dashboard"))
        error = "Invalid admin credentials"
    return render_template("login_admin.html", form=form, error=error)


# -----------------------
# SUPERVISOR LOGIN
# -----------------------
@auth_bp.route("/supervisor/login", methods=["GET", "POST"])
def supervisor_login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, role="supervisor").first()
        if user and check_password(user.password, form.password.data):
            session["user_id"] = user.id
            session["role"] = user.role
            return redirect(url_for("supervisor.dashboard"))
        error = "Invalid supervisor credentials"
    return render_template("login_supervisor.html", form=form, error=error)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.index"))
