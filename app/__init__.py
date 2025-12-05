import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.Config")

    # Ensure instance & upload folders exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

        # Create default admin & supervisor if not present
        from .models import User
        from .utils import hash_password

        if not User.query.filter_by(email="admin@spms.com").first():
            admin = User(
                fullname="Default Admin",
                email="admin@spms.com",
                password=hash_password("admin123"),
                role="admin",
            )
            db.session.add(admin)

        if not User.query.filter_by(email="supervisor@spms.com").first():
            sup = User(
                fullname="Default Supervisor",
                email="supervisor@spms.com",
                password=hash_password("supervisor123"),
                role="supervisor",
            )
            db.session.add(sup)

        db.session.commit()

        # Register blueprints
        from .auth_routes import auth_bp
        from .student_routes import student_bp
        from .admin_routes import admin_bp
        from .supervisor_routes import supervisor_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(student_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(supervisor_bp)

        return app
