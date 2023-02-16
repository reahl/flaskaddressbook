import pathlib
from flask import Flask, render_template, redirect, url_for, abort
from flask_bootstrap import Bootstrap4
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length
from sqlalchemy import Column, Integer, UnicodeText
from sqlalchemy.exc import NoResultFound
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///address.db"
# app.config['SQLALCHEMY_ECHO'] = True

# For Flask-WTF CSRF
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'


db.init_app(app)

Bootstrap4(app)

class AddressForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email_address = EmailField('Email', validators=[DataRequired()])
    save = SubmitField('Save')


class Address(db.Model):
    __tablename__ = 'parameterised1_address'

    id            = Column(Integer, primary_key=True)
    email_address = Column(UnicodeText)
    name          = Column(UnicodeText)

    def save(self):
        db.session.add(self)

if not pathlib.Path('address.db').exists():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    addresses = db.session.query(Address).all()
    return render_template('index.html', addresses=addresses)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddressForm()

    if form.validate_on_submit():

        name = form.name.data
        email_address = form.email_address.data

        Address(name=name, email_address=email_address).save()
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):

    try:
        address = db.session.query(Address).filter_by(id=id).one()
    except NoResultFound:
        abort(404)

    form = AddressForm()
    if form.is_submitted():
        if form.validate_on_submit():

            name = form.name.data
            email_address = form.email_address.data

            address.name = name
            address.email_address = email_address
            db.session.commit()

            return redirect(url_for('index'))
    else:
        form = AddressForm(obj=address)

    return render_template('edit.html', form=form)
