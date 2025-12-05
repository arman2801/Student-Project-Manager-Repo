import bcrypt
from werkzeug.utils import secure_filename
import os
from flask import current_app

def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def check_password(hashed, plain):
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

def save_uploaded_file(file_storage):
    if not file_storage:
        return None

    filename = secure_filename(file_storage.filename)
    if filename == "":
        return None

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    path = os.path.join(upload_folder, filename)
    file_storage.save(path)

    # store relative file name only
    return filename
