import random
from flask import Blueprint, request, jsonify
from auth import require_api_token
from generators.base import s1_id, s1_uuid, s1_timestamp, random_count, fake
from config import Config

misc_bp = Blueprint('misc', __name__)


def generate_marketplace_app():
    return {
        'id': s1_uuid(),
        'name': random.choice([
            'SentinelOne EDR', 'Threat Intelligence', 'Cloud Security Posture',
            'Identity Security', 'Network Detection', 'Vulnerability Assessment',
        ]),
        'version': fake.numerify('#.#.#'),
        'status': random.choice(['installed', 'available', 'deprecated']),
        'vendor': 'SentinelOne',
        'description': fake.sentence(nb_words=12),
        'installedAt': s1_timestamp(days_back=200),
        'siteId': random.choice(Config.SITE_IDS),
    }


def generate_service_user():
    return {
        'id': s1_id(),
        'name': fake.name() + ' (Service)',
        'description': fake.sentence(nb_words=8),
        'createdAt': s1_timestamp(days_back=300),
        'updatedAt': s1_timestamp(days_back=30),
        'creator': 'admin@acme.com',
        'creatorId': s1_id(),
        'expiration': None,
        'apiToken': {
            'createdAt': s1_timestamp(days_back=100),
            'expiresAt': '2027-12-31T00:00:00.000000Z',
        },
        'scope': 'account',
        'scopeName': 'Acme Corp',
    }


@misc_bp.route('/web/api/v<version>/singularity-marketplace/applications', methods=['GET'])
@require_api_token
def list_marketplace_apps(version):
    count = int(request.args.get('limit', random_count(2, 8)))
    apps = [generate_marketplace_app() for _ in range(min(count, 20))]
    return jsonify({
        'data': apps,
        'pagination': {'totalItems': len(apps), 'nextCursor': None},
        'errors': None,
    }), 200


@misc_bp.route('/web/api/v<version>/service-users', methods=['GET'])
@require_api_token
def get_service_users(version):
    count = int(request.args.get('limit', random_count(1, 5)))
    users = [generate_service_user() for _ in range(min(count, 10))]
    return jsonify({
        'data': users,
        'pagination': {'totalItems': len(users), 'nextCursor': None},
        'errors': None,
    }), 200


@misc_bp.route('/web/api/v<version>/agents/mac', methods=['GET'])
@require_api_token
def get_agent_mac(version):
    from generators.base import mac_address, private_ip
    data = {
        'macAddress': mac_address(),
        'ipAddress': private_ip(),
    }
    return jsonify({'data': data, 'errors': None}), 200
