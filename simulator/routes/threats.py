import random
from flask import Blueprint, request, jsonify, Response
from auth import require_api_token
from generators.base import s1_response, s1_affected, s1_id, random_count
from generators.threats import (
    generate_threat, generate_threat_note,
    generate_threat_summary, generate_threat_analysis,
)

threats_bp = Blueprint('threats', __name__)


@threats_bp.route('/web/api/v<version>/threats', methods=['GET'])
@require_api_token
def get_threats(version):
    count = int(request.args.get('limit', random_count()))
    threats = [generate_threat() for _ in range(min(count, 50))]
    return jsonify(s1_response(threats)), 200


@threats_bp.route('/web/api/v<version>/threats/mark-as-threat', methods=['POST'])
@require_api_token
def mark_as_threat(version):
    return jsonify(s1_affected(random.randint(1, 5))), 200


@threats_bp.route('/web/api/v<version>/threats/mitigate/<action>', methods=['POST'])
@require_api_token
def mitigate_threat(version, action):
    return jsonify(s1_affected(random.randint(1, 5))), 200


@threats_bp.route('/web/api/v<version>/threats/mark-as-resolved', methods=['POST'])
@require_api_token
def resolve_threat(version):
    return jsonify(s1_affected(random.randint(1, 5))), 200


@threats_bp.route('/web/api/v<version>/threats/analyst-verdict', methods=['POST'])
@require_api_token
def update_threats_verdict(version):
    return jsonify(s1_affected(random.randint(1, 5))), 200


@threats_bp.route('/web/api/v<version>/threats/incident', methods=['POST'])
@require_api_token
def update_threats_status(version):
    return jsonify(s1_affected(random.randint(1, 5))), 200


@threats_bp.route('/web/api/v<version>/threats/notes', methods=['POST'])
@require_api_token
def write_threat_note(version):
    body = request.get_json() or {}
    threat_ids = body.get('filter', {}).get('ids', [s1_id()])
    notes = []
    for tid in (threat_ids if isinstance(threat_ids, list) else [threat_ids]):
        notes.append(generate_threat_note(tid))
    return jsonify(s1_response(notes)), 200


@threats_bp.route('/web/api/v<version>/threats/<threat_id>/notes', methods=['GET'])
@require_api_token
def get_threat_notes(version, threat_id):
    count = random_count(1, 5)
    notes = [generate_threat_note(threat_id) for _ in range(count)]
    return jsonify(s1_response(notes)), 200


@threats_bp.route('/web/api/v<version>/threats/<threat_id>/timeline', methods=['GET'])
@require_api_token
def threat_timeline(version, threat_id):
    from generators.base import s1_timestamp, fake
    count = random_count(3, 10)
    events = [
        {
            'id': s1_id(),
            'hash': None,
            'threatId': threat_id,
            'type': random.choice(['CREATED', 'UPDATED', 'MITIGATED', 'RESOLVED']),
            'activityType': random.randint(3001, 3013),
            'description': fake.sentence(nb_words=10),
            'createdAt': s1_timestamp(days_back=30),
            'updatedAt': s1_timestamp(days_back=7),
        }
        for _ in range(count)
    ]
    return jsonify(s1_response(events)), 200


@threats_bp.route('/web/api/v<version>/threats/fetch-file', methods=['POST'])
@require_api_token
def fetch_threat_file(version):
    return jsonify({'data': {'success': True}, 'errors': None}), 200


@threats_bp.route('/web/api/v<version>/threats/<threat_id>/download-from-cloud', methods=['GET'])
@require_api_token
def download_threat_from_cloud(version, threat_id):
    content = b'SIMULATED_THREAT_FILE_CONTENT'
    return Response(content, mimetype='application/octet-stream',
                    headers={'Content-Disposition': 'attachment; filename=threat_file.bin'})


@threats_bp.route('/web/api/v<version>/private/threats/summary', methods=['GET'])
@require_api_token
def threat_summary(version):
    return jsonify(generate_threat_summary()), 200


@threats_bp.route('/web/api/v<version>/private/threats/<threat_id>/analysis', methods=['GET'])
@require_api_token
def threat_analysis(version, threat_id):
    return jsonify(generate_threat_analysis(threat_id)), 200
