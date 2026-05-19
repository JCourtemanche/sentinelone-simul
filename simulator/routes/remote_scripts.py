import random
from flask import Blueprint, request, jsonify
from auth import require_api_token
from generators.base import s1_id, s1_uuid, s1_timestamp, fake

remote_scripts_bp = Blueprint('remote_scripts', __name__)

TASK_STATUSES = ['pending', 'running', 'completed', 'failed']


def generate_task_status(task_id=None):
    return {
        'taskId': task_id or s1_uuid(),
        'status': random.choice(TASK_STATUSES),
        'completionDate': s1_timestamp(days_back=1),
        'agentId': s1_id(),
        'computerName': 'DESKTOP-' + fake.lexify('????????').upper(),
        'initiatedAt': s1_timestamp(days_back=2),
        'updatedAt': s1_timestamp(days_back=1),
        'type': 'remoteScriptExecution',
    }


@remote_scripts_bp.route('/web/api/v<version>/remote-scripts/execute', methods=['POST'])
@require_api_token
def run_remote_script(version):
    task_id = s1_uuid()
    return jsonify({
        'data': {
            'pendingTaskIds': [task_id],
            'affected': 1,
        },
        'errors': None,
    }), 200


@remote_scripts_bp.route('/web/api/v<version>/remote-scripts/status', methods=['GET'])
@require_api_token
def get_remote_script_status(version):
    count = int(request.args.get('limit', 5))
    statuses = [generate_task_status() for _ in range(min(count, 10))]
    return jsonify({
        'data': statuses,
        'pagination': {'totalItems': len(statuses), 'nextCursor': None},
        'errors': None,
    }), 200


@remote_scripts_bp.route('/web/api/v<version>/remote-scripts/fetch-files', methods=['POST'])
@require_api_token
def get_remote_script_results(version):
    return jsonify({
        'data': {
            'download_url': 'https://example.com/results.zip',
            'fileName': 'script_results.zip',
        },
        'errors': None,
    }), 200
