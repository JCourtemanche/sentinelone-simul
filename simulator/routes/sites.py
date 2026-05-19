import random
from flask import Blueprint, request, jsonify
from auth import require_api_token
from generators.base import s1_response, s1_affected, s1_id, s1_timestamp
from generators.sites import generate_site, generate_all_sites

sites_bp = Blueprint('sites', __name__)


@sites_bp.route('/web/api/v<version>/sites', methods=['GET'])
@require_api_token
def get_sites(version):
    sites = generate_all_sites()
    return jsonify({
        'data': {
            'sites': sites,
            'allSites': {
                'totalLicenses': 3000,
                'activeLicenses': random.randint(500, 2500),
            },
        },
        'pagination': {'totalItems': len(sites), 'nextCursor': None},
        'errors': None,
    }), 200


@sites_bp.route('/web/api/v<version>/sites/<site_id>', methods=['GET'])
@require_api_token
def get_site(version, site_id):
    from config import Config
    idx = Config.SITE_IDS.index(site_id) if site_id in Config.SITE_IDS else 0
    site = generate_site(site_id=site_id, idx=idx)
    return jsonify({'data': site, 'errors': None}), 200


@sites_bp.route('/web/api/v<version>/sites/<site_id>/reactivate', methods=['PUT'])
@require_api_token
def reactivate_site(version, site_id):
    return jsonify(s1_affected(1)), 200


@sites_bp.route('/web/api/v<version>/sites/<site_id>/expire-now', methods=['POST'])
@require_api_token
def expire_site(version, site_id):
    return jsonify(s1_affected(1)), 200
