import os

from flask import Flask, render_template, abort, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

from app.services.contact_service import ContactService

from .auth import UserService

DATABASE_URL = os.environ.get("DATABASE_URL", "data/contacts.json")

app = Flask(__name__)
app.config["SECRET_KEY"] = "36e7c3a9e093232db56749db8fcc1915a5c2e9e810fb7df243f496c19abf25e1"

contact_service = ContactService(DATABASE_URL)
login_manager = LoginManager(app)
user_service = UserService()

login_manager.login_view = "login"


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    number = StringField('Number', validators=[DataRequired()])
    

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = user_service.get_by_username(form.username.data)
        if user is None:
            return render_template("login.html", form=form, message="Unknown username or password")

        if user.password != form.password.data:
            return render_template("login.html", form=form, message="Unknown username or password")

        login_user(user)

        _next = request.args.get("next", "")

        return redirect(_next or url_for("index"))

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.route("/")
def index():
    contacts = contact_service.get_contacts()
    return render_template("index.html", contacts=contacts)


@app.route("/search/")
@login_required
def search():
    term = request.args.get('term', '')

    if not term:
        return redirect(url_for("index"))
    contacts = contact_service.find(term)
    return render_template("search.html", contacts=contacts, term=term)


@app.route("/about-us")
def about():
    return render_template("about.html")


@app.route("/contacts/add", methods=["GET", "POST"])
@login_required
def add_contact():
    form = ContactForm()

    if form.validate_on_submit():
        contact = contact_service.create(
            form.name.data,
            form.email.data,
            form.number.data
        )
        return redirect(url_for("contact_details", name=contact.name))

    return render_template("add_contact.html", form=form)


@app.route("/contacts/<name>/")
@login_required
def contact_details(name):
    try:
        contact = contact_service.find(name)[0]
    except IndexError:
        return abort(404)

    return render_template("contact_details.html", contact=contact)


@app.route("/contacts/<name>/edit", methods=["GET", "POST"])
@login_required
def edit_contact(name):
    try:
        contact = contact_service.find(name)[0]
    except IndexError:
        return abort(404)

    form = ContactForm(obj=contact)

    if form.validate_on_submit():
        form.populate_obj(contact)
        contact_service.save_contacts()

        return redirect(url_for("contact_details", name=contact.name))

    return render_template("edit_contact.html", contact=contact, form=form)


@app.route("/contacts/<name>/remove", methods=["POST"])
@login_required
def remove_contact(name):
    try:
        contact = contact_service.find(name)[0]
    except IndexError:
        return abort(404)

    contact_service.remove(contact)

    return redirect(url_for("index"))


@login_manager.user_loader
def load_user(user_id):
    return user_service.get_by_id(int(user_id))



