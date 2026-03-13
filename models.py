"""
AstroGuy AI — SQLAlchemy Database Models
=========================================
Tables:
  - users          : registered user accounts
  - birth_charts   : saved birth chart calculations
  - compatibility_reports : saved compatibility results
  - feedback       : user feedback submissions
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

db   = SQLAlchemy()
bcrypt = Bcrypt()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(180), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    gender        = db.Column(db.String(10))
    language      = db.Column(db.String(5), default="en")
    dark_mode     = db.Column(db.Boolean, default=False)
    reset_token   = db.Column(db.String(256), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    last_login    = db.Column(db.DateTime)

    # Relationships
    birth_charts   = db.relationship("BirthChart",   backref="user", lazy=True, cascade="all, delete-orphan")
    compat_reports = db.relationship("CompatibilityReport", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


class BirthChart(db.Model):
    __tablename__ = "birth_charts"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    label      = db.Column(db.String(100), default="My Chart")
    # Birth details
    full_name  = db.Column(db.String(100))
    dob        = db.Column(db.String(20))          # "YYYY-MM-DD"
    birth_time = db.Column(db.String(10))          # "HH:MM"
    birth_place= db.Column(db.String(200))
    gender     = db.Column(db.String(10))
    latitude   = db.Column(db.Float)
    longitude  = db.Column(db.Float)
    timezone   = db.Column(db.String(60))
    # Calculated results stored as JSON string
    chart_json = db.Column(db.Text)                # JSON of calculate_birth_chart()
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<BirthChart {self.full_name} {self.dob}>"


class CompatibilityReport(db.Model):
    __tablename__ = "compatibility_reports"

    id       = db.Column(db.Integer, primary_key=True)
    user_id  = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name1    = db.Column(db.String(100))
    dob1     = db.Column(db.String(20))
    time1    = db.Column(db.String(10))
    place1   = db.Column(db.String(200))
    name2    = db.Column(db.String(100))
    dob2     = db.Column(db.String(20))
    time2    = db.Column(db.String(10))
    place2   = db.Column(db.String(200))
    score    = db.Column(db.Float)
    result_json = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CompatReport {self.name1} & {self.name2}>"


class Feedback(db.Model):
    __tablename__ = "feedback"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    rating     = db.Column(db.Integer)             # 1-5
    category   = db.Column(db.String(50))          # "bug" / "feature" / "general"
    message    = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Feedback {self.rating} {self.category}>"
