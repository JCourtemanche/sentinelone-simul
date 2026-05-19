import random
from flask import Blueprint, request, jsonify
from auth import require_api_token
from generators.base import s1_response, s1_uuid, s1_timestamp, sha256, public_ip, fake, random_count

dv_bp = Blueprint('dv', __name__)

# In-memory store for query IDs (simulates async queries)
_queries = {}


def generate_dv_event():
    return {
        'eventType': random.choice(['Process Creation', 'Network Connection', 'File Creation', 'Registry Key Set']),
        'eventTime': s1_timestamp(days_back=7),
        'agentId': str(random.randint(100000000000000000, 999999999999999999)),
        'agentComputerName': 'DESKTOP-' + fake.lexify('????????').upper(),
        'agentOs': random.choice(['windows', 'macos', 'linux']),
        'srcProcUser': fake.user_name(),
        'srcProcName': random.choice(['powershell.exe', 'cmd.exe', 'python.exe', 'chrome.exe']),
        'srcProcPid': random.randint(1000, 65535),
        'srcProcSha256': sha256(),
        'networkUrl': random.choice([None, 'https://' + fake.domain_name()]),
        'networkRemoteIp': public_ip(),
        'networkRemotePort': random.choice([80, 443, 8080, 53, 4444]),
        'fileFullName': random.choice([
            'C:\\Temp\\payload.exe',
            '/tmp/script.sh',
            'C:\\Users\\user\\Downloads\\document.pdf',
        ]),
        'fileSha256': sha256(),
        'fileMd5': None,
        'trueContext': s1_uuid(),
        'id': s1_uuid(),
    }


def generate_dv_process():
    return {
        'processName': random.choice(['powershell.exe', 'cmd.exe', 'bash', 'python3']),
        'pid': random.randint(1000, 65535),
        'parentPid': random.randint(100, 999),
        'user': fake.user_name(),
        'startTime': s1_timestamp(days_back=1),
        'cmdLine': fake.sentence(nb_words=8),
        'sha256': sha256(),
        'agentId': str(random.randint(100000000000000000, 999999999999999999)),
        'agentComputerName': 'DESKTOP-' + fake.lexify('????????').upper(),
        'id': s1_uuid(),
        'trueContext': s1_uuid(),
    }


@dv_bp.route('/web/api/v<version>/dv/init-query', methods=['POST'])
@require_api_token
def create_query(version):
    query_id = s1_uuid()
    _queries[query_id] = {'status': 'RUNNING', 'progress': 0}
    return jsonify({'data': {'queryId': query_id}, 'errors': None}), 200


@dv_bp.route('/web/api/v<version>/dv/query-status', methods=['GET'])
@require_api_token
def get_query_status(version):
    query_id = request.args.get('queryId', s1_uuid())
    if query_id in _queries:
        _queries[query_id]['progress'] = min(100, _queries[query_id]['progress'] + 50)
        status = 'FINISHED' if _queries[query_id]['progress'] >= 100 else 'RUNNING'
        _queries[query_id]['status'] = status
    else:
        status = 'FINISHED'
    return jsonify({'data': {'status': status, 'responseState': status, 'progress': 100}, 'errors': None}), 200


@dv_bp.route('/web/api/v<version>/dv/events', methods=['GET'])
@require_api_token
def get_events(version):
    count = int(request.args.get('limit', random_count()))
    events = [generate_dv_event() for _ in range(min(count, 50))]
    return jsonify(s1_response(events)), 200


@dv_bp.route('/web/api/v<version>/dv/events/process', methods=['GET'])
@require_api_token
def get_processes(version):
    count = int(request.args.get('limit', random_count()))
    processes = [generate_dv_process() for _ in range(min(count, 50))]
    return jsonify(s1_response(processes)), 200


@dv_bp.route('/web/api/v<version>/dv/events/pq', methods=['POST'])
@require_api_token
def run_power_query(version):
    query_id = s1_uuid()
    return jsonify({'data': {'queryId': query_id, 'status': 'RUNNING'}, 'errors': None}), 200


@dv_bp.route('/web/api/v<version>/dv/events/pq', methods=['GET'])
@require_api_token
def get_power_query_results(version):
    count = int(request.args.get('limit', random_count()))
    rows = [
        {'columns': [fake.word(), str(random.randint(0, 1000)), fake.ipv4_public()]}
        for _ in range(min(count, 20))
    ]
    return jsonify({
        'data': {
            'status': 'FINISHED',
            'columns': [{'name': 'event_type'}, {'name': 'count'}, {'name': 'src_ip'}],
            'data': rows,
        },
        'errors': None,
    }), 200


@dv_bp.route('/web/api/v<version>/dv/events/pq-ping', methods=['GET'])
@require_api_token
def ping_power_query(version):
    return jsonify({'data': {'status': 'FINISHED', 'progress': 100}, 'errors': None}), 200
