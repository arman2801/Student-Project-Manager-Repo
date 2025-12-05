from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    SelectField
)
from wtforms.validators import InputRequired, Email, Length
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    fullname = StringField("Full Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])
    submit = SubmitField("Register")


class TaskAssignForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    student = SelectField("Assign To (Student)", coerce=int)
    due_date = StringField("Due Date (e.g. 2025-12-31)", validators=[InputRequired()])
    submit = SubmitField("Assign Task")


class TaskEditForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    due_date = StringField("Due Date", validators=[InputRequired()])
    status = SelectField("Status", choices=[
        ("Pending", "Pending"),
        ("Submitted", "Submitted"),
        ("Reviewed", "Reviewed")
    ])
    submit = SubmitField("Update Task")


class SubmissionForm(FlaskForm):
    submission_text = TextAreaField("Your Answer")
    file = FileField("Upload File", validators=[FileAllowed(["pdf", "doc", "docx", "txt", "png", "jpg", "jpeg"])])
    submit = SubmitField("Submit")
