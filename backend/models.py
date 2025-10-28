from datetime import datetime
from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="viewer")
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    defects_assigned = db.relationship("Defect", back_populates="assignee", lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    defects = db.relationship("Defect", back_populates="project", lazy=True, cascade="all, delete-orphan")
