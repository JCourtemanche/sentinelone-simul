import random
from flask import Blueprint, request, jsonify
from auth import require_api_token
from generators.base import s1_response, s1_affected, s1_id, s1_timestamp, random_count, fake

exclusions_bp = Blueprint('exclusions', __name__)

EXCLUSION_TYPES = ['file_type', 'path', 'white_hash', 'certificate', 'browser']
OS_TYPES = ['windows', 'macos', 'linux']


def generate_exclusion():
    return {
        'id': s1_id(),
        'type': random.choice(EXCLUSION_TYPES),
        'value': random.choice([
            '*.log', 'C:\\Tools\\scanner.exe', 'abc123def456' * 3,
            '/opt/security/', 'trusted-cert.pem',
        ]),
        'osType': random.choice(OS_TYPES),
        'description': fake.sentence(nb_words=6),
        'createdAt': s1_timestamp(days_back=200),
        'updatedAt': s1_timestamp(days_back=30),
        'createdBy': fake.email(),
        'userId': s1_id(),
        'siteId': None,
        'groupIds': [],
        'mode': random.choice(['suppress', 'disable_in_process_monitor', None]),
        'pathExclusionType': None,
        'source': 'user',
        'status': 'active',
    }


@exclusions_bp.route('/web/api/v<version>/exclusions', methods=['GET'])
@require_api_token
def get_whitelist(version):
    count = int(request.args.get('limit', random_count()))
    items = [generate_exclusion() for _ in range(min(count, 50))]
    return jsonify(s1_response(items)), 200


@exclusions_bp.route('/web/api/v<version>/exclusions', methods=['POST'])
@require_api_token
def create_whitelist_item(version):
    item = generate_exclusion()
    return jsonify({'data': item, 'errors': None}), 200


@exclusions_bp.route('/web/api/v<version>/exclusions', methods=['DELETE'])
@require_api_token
def remove_whitelist_item(version):
    return jsonify(s1_affected(random.randint(1, 3))), 200
