import random
from flask import Blueprint, request, jsonify
from auth import require_api_token
from generators.base import s1_response, s1_affected, random_count
from generators.alerts import generate_alert

alerts_bp = Blueprint('alerts', __name__)


@alerts_bp.route('/web/api/v<version>/cloud-detection/alerts', methods=['GET'])
@require_api_token
def get_alerts(version):
    count = int(request.args.get('limit', random_count()))
    alerts = [generate_alert() for _ in range(min(count, 50))]
    return jsonify(s1_response(alerts)), 200


@alerts_bp.route('/web/api/v<version>/cloud-detection/alerts/analyst-verdict', methods=['POST'])
@require_api_token
def update_alerts_verdict(version):
    return jsonify(s1_affected(random.randint(1, 5))), 200


@alerts_bp.route('/web/api/v<version>/cloud-detection/alerts/incident', methods=['POST'])
@require_api_token
def update_alerts_status(version):
    return jsonify(s1_affected(random.randint(1, 5))), 200
