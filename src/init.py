"""Project initialization."""
from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from dotenv import load_dotenv


# Initialize Flask app
app = Flask(__name__)
load_dotenv()
app.secret_key = getenv('SECRET_KEY')

# Initialize db
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Reference(db.Model):  # pylint: disable=too-few-public-methods
    """ORM database table for references."""
    __tablename__ = 'reference'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String)
    title = db.Column(db.String)
    booktitle = db.Column(db.String)
    year = db.Column(db.Integer)
    type_id = db.Column(db.Integer,db.ForeignKey('type.id'))
    type = relationship('Type', viewonly=True)


class Type(db.Model):  # pylint: disable=too-few-public-methods
    """ORM database table for reference types."""
    __tablename__ = 'type'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)


# Make sure tables exist
with app.app_context():
    db.create_all()

    # Add new reference to the list below, they will be added to database
    # and ignored if they already exist.
    # Hardcode id to prevent differences between testing and production.
    types = [
        Type(id=1, name='InCollection'),
        Type(id=2, name='Book')
    ]

    for type_ in types:
        same_type = Type.query.filter_by(name=type_.name).first()
        if same_type:
            continue
        db.session.add(type_)  # pylint: disable=no-member
    db.session.commit()  # pylint: disable=no-member
