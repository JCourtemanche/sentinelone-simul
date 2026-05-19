import random
from flask import Blueprint, request, jsonify
from auth import require_api_token
from generators.base import s1_response, s1_affected, s1_id, random_count
from generators.agents import generate_agent, generate_agent_process, generate_installed_application

agents_bp = Blueprint('agents', __name__)


@agents_bp.route('/web/api/v<version>/agents', methods=['GET'])
@require_api_token
def list_agents(version):
    count = int(request.args.get('limit', random_count()))
    agents = [generate_agent() for _ in range(min(count, 50))]
    return jsonify(s1_response(agents)), 200


@agents_bp.route('/web/api/v<version>/agents/processes', methods=['GET'])
@require_api_token
def agent_processes(version):
    agent_id = request.args.get('ids', s1_id())
    count = random_count(3, 15)
    processes = [generate_agent_process(agent_id) for _ in range(count)]
    return jsonify(s1_response(processes)), 200


@agents_bp.route('/web/api/v<version>/agents/applications', methods=['GET'])
@require_api_token
def installed_applications(version):
    count = random_count(5, 20)
    apps = [generate_installed_application() for _ in range(count)]
    return jsonify(s1_response(apps)), 200


@agents_bp.route('/web/api/v<version>/agents/actions/connect', methods=['POST'])
@require_api_token
def connect_agent(version):
    return jsonify(s1_affected(random.randint(1, 5))), 200


@agents_bp.route('/web/api/v<version>/agents/actions/disconnect', methods=['POST'])
@require_api_token
def disconnect_agent(version):
    return jsonify(s1_affected(random.randint(1, 5))), 200


@agents_bp.route('/web/api/v<version>/agents/actions/broadcast', methods=['POST'])
@require_api_token
def broadcast_message(version):
    return jsonify(s1_affected(random.randint(1, 10))), 200


@agents_bp.route('/web/api/v<version>/agents/actions/uninstall', methods=['POST'])
@require_api_token
def uninstall_agent(version):
    return jsonify(s1_affected(random.randint(1, 3))), 200


@agents_bp.route('/web/api/v<version>/agents/actions/shutdown', methods=['POST'])
@require_api_token
def shutdown_agent(version):
    return jsonify(s1_affected(random.randint(1, 3))), 200


@agents_bp.route('/web/api/v<version>/agents/actions/initiate-scan', methods=['POST'])
@require_api_token
def initiate_scan(version):
    return jsonify(s1_affected(random.randint(1, 5))), 200


@agents_bp.route('/web/api/v<version>/agents/actions/abort-scan', methods=['POST'])
@require_api_token
def abort_scan(version):
    return jsonify(s1_affected(random.randint(1, 5))), 200


@agents_bp.route('/web/api/v<version>/agents/actions/fetch-logs', methods=['POST'])
@require_api_token
def fetch_logs(version):
    return jsonify(s1_affected(random.randint(1, 3))), 200


@agents_bp.route('/web/api/v<version>/agents/<agent_id>/actions/fetch-files', methods=['POST'])
@require_api_token
def fetch_files(version, agent_id):
    return jsonify({'data': {'success': True}, 'errors': None}), 200


@agents_bp.route('/web/api/v<version>/agents/<agent_id>/uploads/<activity_id>', methods=['GET'])
@require_api_token
def download_fetched_file(version, agent_id, activity_id):
    # Return a fake ZIP file content (minimal valid ZIP header)
    zip_bytes = (
        b'PK\x03\x04\x14\x00\x00\x00\x08\x00'
        b'\x00\x00!\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x0b\x00\x00\x00fetched.txtHello World'
        b'PK\x01\x02\x14\x03\x14\x00\x00\x00\x08\x00'
        b'\x00\x00!\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00fetched.txt'
        b'PK\x05\x06\x00\x00\x00\x00\x01\x00\x01\x009\x00\x00\x00'
        b'4\x00\x00\x00\x00\x00'
    )
    from flask import Response
    return Response(zip_bytes, mimetype='application/zip',
                    headers={'Content-Disposition': 'attachment; filename=fetched.zip'})
