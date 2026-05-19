import random
from flask import Blueprint, request, jsonify
from auth import require_api_token
from generators.base import s1_response, s1_affected
from generators.groups import generate_all_groups

groups_bp = Blueprint('groups', __name__)


@groups_bp.route('/web/api/v<version>/groups', methods=['GET'])
@require_api_token
def get_groups(version):
    groups = generate_all_groups()
    return jsonify(s1_response(groups)), 200


@groups_bp.route('/web/api/v<version>/groups/<group_id>', methods=['DELETE'])
@require_api_token
def delete_group(version, group_id):
    return jsonify(s1_affected(1)), 200


@groups_bp.route('/web/api/v<version>/groups/<group_id>/move-agents', methods=['PUT'])
@require_api_token
def move_agent(version, group_id):
    return jsonify(s1_affected(random.randint(1, 5))), 200
