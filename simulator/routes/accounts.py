import random
from flask import Blueprint, request, jsonify
from auth import require_api_token
from generators.base import s1_response, s1_timestamp
from config import Config

accounts_bp = Blueprint('accounts', __name__)


def generate_account(account_id=None):
    return {
        'id': account_id or Config.ACCOUNT_IDS[0],
        'name': 'Acme Corp',
        'accountType': 'Paid',
        'state': 'active',
        'activeAgents': random.randint(100, 1000),
        'totalAgents': random.randint(1000, 2000),
        'activeLicenses': random.randint(500, 1500),
        'totalLicenses': 2000,
        'unlimitedLicenses': False,
        'expiration': None,
        'createdAt': s1_timestamp(days_back=1000),
        'updatedAt': s1_timestamp(days_back=30),
        'isDefault': True,
        'numberOfSites': len(Config.SITE_IDS),
    }


@accounts_bp.route('/web/api/v<version>/accounts', methods=['GET'])
@require_api_token
def get_accounts(version):
    accounts = [generate_account()]
    return jsonify(s1_response(accounts)), 200


@accounts_bp.route('/web/api/v<version>/accounts/<account_id>', methods=['GET'])
@require_api_token
def get_account(version, account_id):
    acc = generate_account(account_id=account_id)
    return jsonify({'data': acc, 'errors': None}), 200
