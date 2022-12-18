import datetime
from app import db


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    username = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        nullable=False
    )
    name = db.Column(
        db.String(60),
        nullable=False
    )
    email = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )
    company_id = db.Column(
        db.Integer,
        db.ForeignKey('companies.id'),
        nullable=False
    )

    created_on = db.Column(
        db.DateTime,
        default=datetime.datetime.now()
    )

    def __init__(
        self,
        username,
        password,
        name,
        email,
        company_id
    ):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.company_id = company_id
