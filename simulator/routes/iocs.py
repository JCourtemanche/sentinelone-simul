import random
from flask import Blueprint, request, jsonify
from auth import require_api_token
from generators.base import s1_response, s1_affected, s1_id, s1_uuid, s1_timestamp, sha256, public_ip, random_count, fake

iocs_bp = Blueprint('iocs', __name__)

IOC_TYPES = ['IPV4', 'IPV6', 'DNS', 'SHA256', 'URL']
METHODS = ['EQUALS', 'CONTAINS']
CATEGORIES = ['MALWARE', 'PHISHING', 'C2', 'EXPLOIT', 'RANSOMWARE']


def _ioc_value(ioc_type):
    if ioc_type == 'IPV4':
        return public_ip()
    elif ioc_type == 'IPV6':
        return fake.ipv6()
    elif ioc_type == 'DNS':
        return 'malicious-' + fake.domain_name()
    elif ioc_type == 'SHA256':
        return sha256()
    else:
        return 'https://malicious-' + fake.domain_name() + '/payload'


def generate_ioc(ioc_id=None):
    ioc_type = random.choice(IOC_TYPES)
    return {
        'uuid': ioc_id or s1_uuid(),
        'type': ioc_type,
        'value': _ioc_value(ioc_type),
        'method': random.choice(METHODS),
        'name': fake.sentence(nb_words=4).rstrip('.'),
        'description': fake.sentence(nb_words=10),
        'category': random.choice(CATEGORIES),
        'source': random.choice(['manual', 'threat-intelligence', 'custom']),
        'externalId': None,
        'creator': fake.email(),
        'creatorId': s1_id(),
        'scope': random.choice(['account', 'global']),
        'scopeId': s1_id(),
        'batchId': s1_uuid(),
        'validUntil': '2027-01-01T00:00:00.000000Z',
        'creationTime': s1_timestamp(days_back=30),
        'updatedAt': s1_timestamp(days_back=7),
    }


@iocs_bp.route('/web/api/v<version>/threat-intelligence/iocs', methods=['GET'])
@require_api_token
def get_iocs(version):
    count = int(request.args.get('limit', random_count()))
    iocs = [generate_ioc() for _ in range(min(count, 50))]
    return jsonify(s1_response(iocs)), 200


@iocs_bp.route('/web/api/v<version>/threat-intelligence/iocs', methods=['POST'])
@require_api_token
def create_ioc(version):
    body = request.get_json() or {}
    # Support both single and bulk IOC creation
    data = body.get('data', [{}])
    if isinstance(data, dict):
        data = [data]
    iocs = [generate_ioc() for _ in data]
    return jsonify({'data': iocs, 'errors': None}), 200


@iocs_bp.route('/web/api/v<version>/threat-intelligence/iocs', methods=['DELETE'])
@require_api_token
def delete_ioc(version):
    return jsonify(s1_affected(random.randint(1, 5))), 200
