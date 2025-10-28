from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database import db
from models import Project
from utils import role_required

bp = Blueprint("projects", __name__, url_prefix="/api/projects")

@bp.get("")
@jwt_required()
def list_projects():
    items = Project.query.order_by(Project.created_at.desc()).all()
    return jsonify([{"id": p.id, "name": p.name, "description": p.description} for p in items])
