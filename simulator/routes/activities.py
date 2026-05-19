from flask import Blueprint, request, jsonify
from auth import require_api_token
from generators.base import s1_response, random_count
from generators.activities import generate_activity

activities_bp = Blueprint('activities', __name__)


@activities_bp.route('/web/api/v<version>/activities', methods=['GET'])
@require_api_token
def get_activities(version):
    count = int(request.args.get('limit', random_count()))
    activities = [generate_activity() for _ in range(min(count, 50))]
    return jsonify(s1_response(activities)), 200


@activities_bp.route('/web/api/v<version>/activities/types', methods=['GET'])
@require_api_token
def get_activity_types(version):
    types = [
        {'action': 'Agent Connected', 'id': 4001},
        {'action': 'Agent Disconnected', 'id': 4002},
        {'action': 'Threat Detected', 'id': 3001},
        {'action': 'Threat Quarantined', 'id': 3002},
        {'action': 'Threat Remediated', 'id': 3003},
        {'action': 'Threat Resolved', 'id': 3005},
        {'action': 'Hash Blocked', 'id': 5001},
        {'action': 'Exclusion Created', 'id': 6001},
    ]
    return jsonify(s1_response(types)), 200
