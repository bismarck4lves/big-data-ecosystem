from app import db


class companies(db.Model):
    __tablename__ = "companies"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(255),
        nullable=False
    )

    def __init__(self, name):
        self.name = name
