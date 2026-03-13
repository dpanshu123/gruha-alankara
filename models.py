from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    designs = db.relationship("Design", backref="user", lazy=True)
    bookings = db.relationship("Booking", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Design(db.Model):
    __tablename__ = "designs"

    design_id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )

    image_path = db.Column(db.String(255), nullable=False)
    style_theme = db.Column(db.String(100))
    ai_output = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Furniture(db.Model):
    __tablename__ = "furniture"

    furniture_id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(80))
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))

    bookings = db.relationship("Booking", backref="furniture", lazy=True)


class Booking(db.Model):
    __tablename__ = "bookings"

    booking_id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )

    furniture_id = db.Column(
        db.Integer,
        db.ForeignKey("furniture.furniture_id"),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="pending"
    )

    booking_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )