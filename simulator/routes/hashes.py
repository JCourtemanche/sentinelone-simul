import random
from flask import Blueprint, jsonify
from auth import require_api_token
from generators.base import s1_timestamp

hashes_bp = Blueprint('hashes', __name__)

REPUTATIONS = ['blacklist', 'whitelist', 'undefined']
CLASSIFICATIONS = ['malware', 'pua', 'goodware', 'undefined']
VERDICTS = ['malicious', 'suspicious', 'benign', 'unknown']


@hashes_bp.route('/web/api/v<version>/hashes/<hash_value>/reputation', methods=['GET'])
@require_api_token
def get_hash_reputation(version, hash_value):
    data = {
        'hash': hash_value,
        'reputation': random.choice(REPUTATIONS),
        'rank': random.randint(0, 10),
        'updatedAt': s1_timestamp(days_back=30),
    }
    return jsonify({'data': data, 'errors': None}), 200


@hashes_bp.route('/web/api/v<version>/hashes/<hash_value>/verdict', methods=['GET'])
@require_api_token
def get_hash_verdict(version, hash_value):
    data = {
        'hash': hash_value,
        'verdict': random.choice(VERDICTS),
        'updatedAt': s1_timestamp(days_back=30),
    }
    return jsonify({'data': data, 'errors': None}), 200


@hashes_bp.route('/web/api/v<version>/hashes/<hash_value>/classification', methods=['GET'])
@require_api_token
def get_hash_classification(version, hash_value):
    data = {
        'hash': hash_value,
        'classification': random.choice(CLASSIFICATIONS),
        'classificationSource': random.choice(['cloud', 'static', 'engine']),
        'updatedAt': s1_timestamp(days_back=30),
    }
    return jsonify({'data': data, 'errors': None}), 200
