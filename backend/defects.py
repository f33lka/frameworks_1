from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import or_
from database import db
from models import Defect, Project, User
from utils import role_required

bp = Blueprint("defects", __name__, url_prefix="/api/defects")

ALLOWED_STATUSES = {"new","in_progress","in_review","closed","cancelled"}
ALLOWED_PRIORITIES = {"low","medium","high"}

@bp.get("")
@jwt_required()
def list_defects():
    q = Defect.query
    project_id = request.args.get("project_id", type=int)
    status = request.args.get("status")
    priority = request.args.get("priority")
    assignee_id = request.args.get("assignee_id", type=int)
    search = request.args.get("q","").strip()

    if project_id:
        q = q.filter(Defect.project_id==project_id)
    if status:
        q = q.filter(Defect.status==status)
    if priority:
        q = q.filter(Defect.priority==priority)
    if assignee_id:
        q = q.filter(Defect.assignee_id==assignee_id)
    if search:
        like = f"%{search}%"
        q = q.filter(or_(Defect.title.ilike(like), Defect.description.ilike(like)))

    items = q.order_by(Defect.created_at.desc()).all()
    return jsonify([serialize_defect(d) for d in items])
