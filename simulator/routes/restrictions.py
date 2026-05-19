import random
from flask import Blueprint, request, jsonify
from auth import require_api_token
from generators.base import s1_response, s1_affected, s1_id, s1_timestamp, random_count, sha256, fake

restrictions_bp = Blueprint('restrictions', __name__)

OS_TYPES = ['windows', 'macos', 'linux', 'windows_legacy']


def generate_blocklist_item():
    return {
        'id': s1_id(),
        'type': 'black_hash',
        'value': sha256(),
        'osType': random.choice(OS_TYPES),
        'description': fake.sentence(nb_words=6),
        'createdAt': s1_timestamp(days_back=200),
        'updatedAt': s1_timestamp(days_back=30),
        'createdBy': fake.email(),
        'userId': s1_id(),
        'siteId': None,
        'scopeLevel': 'account',
        'source': 'manual',
    }


@restrictions_bp.route('/web/api/v<version>/restrictions', methods=['GET'])
@require_api_token
def get_blocklist(version):
    count = int(request.args.get('limit', random_count()))
    items = [generate_blocklist_item() for _ in range(min(count, 50))]
    return jsonify(s1_response(items)), 200


@restrictions_bp.route('/web/api/v<version>/restrictions', methods=['POST'])
@require_api_token
def add_to_blocklist(version):
    item = generate_blocklist_item()
    return jsonify({'data': item, 'errors': None}), 200


@restrictions_bp.route('/web/api/v<version>/restrictions', methods=['DELETE'])
@require_api_token
def remove_from_blocklist(version):
    return jsonify(s1_affected(random.randint(1, 3))), 200
