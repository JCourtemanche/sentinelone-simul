import random
from flask import Blueprint, request, jsonify
from auth import require_api_token
from generators.base import s1_response, s1_affected, s1_id, s1_timestamp, random_count, fake

star_bp = Blueprint('star', __name__)

SEVERITIES = ['Low', 'Medium', 'High', 'Critical']
STATUSES = ['Active', 'Activating', 'Draft', 'Disabled', 'Disabling', 'Deleted']
EXPIRATION_MODES = ['Permanent', 'Temporary']


def generate_star_rule(rule_id=None):
    return {
        'id': rule_id or s1_id(),
        'name': fake.sentence(nb_words=4).rstrip('.'),
        'status': random.choice(STATUSES),
        'severity': random.choice(SEVERITIES),
        'description': fake.sentence(nb_words=10),
        'queryType': random.choice(['events', 'processes']),
        's1ql': 'EventType = "Process Creation" AND SrcProcName = "powershell.exe"',
        'networkQuarantine': random.choice([True, False]),
        'treatAsThreat': random.choice(['Malicious', 'Suspicious', 'UNDEFINED']),
        'expirationMode': random.choice(EXPIRATION_MODES),
        'expirationDate': '2027-06-01T00:00:00.000000Z' if random.choice([True, False]) else None,
        'scopeHierarchy': random.choice(['account', 'site', 'group']),
        'createdAt': s1_timestamp(days_back=100),
        'updatedAt': s1_timestamp(days_back=10),
        'creator': fake.name(),
        'creatorId': s1_id(),
        'siteIds': [],
        'groupIds': [],
        'accountIds': [],
    }


@star_bp.route('/web/api/v<version>/cloud-detection/rules', methods=['POST'])
@require_api_token
def create_star_rule(version):
    rule = generate_star_rule()
    return jsonify({'data': rule, 'errors': None}), 200


@star_bp.route('/web/api/v<version>/cloud-detection/rules', methods=['GET'])
@require_api_token
def get_star_rules(version):
    count = int(request.args.get('limit', random_count()))
    rules = [generate_star_rule() for _ in range(min(count, 20))]
    return jsonify(s1_response(rules)), 200


@star_bp.route('/web/api/v<version>/cloud-detection/rules/<rule_id>', methods=['PUT'])
@require_api_token
def update_star_rule(version, rule_id):
    rule = generate_star_rule(rule_id=rule_id)
    return jsonify({'data': rule, 'errors': None}), 200


@star_bp.route('/web/api/v<version>/cloud-detection/rules/enable', methods=['PUT'])
@require_api_token
def enable_star_rules(version):
    return jsonify(s1_affected(random.randint(1, 5))), 200


@star_bp.route('/web/api/v<version>/cloud-detection/rules/disable', methods=['PUT'])
@require_api_token
def disable_star_rules(version):
    return jsonify(s1_affected(random.randint(1, 5))), 200


@star_bp.route('/web/api/v<version>/cloud-detection/rules', methods=['DELETE'])
@require_api_token
def delete_star_rule(version):
    return jsonify(s1_affected(random.randint(1, 3))), 200
