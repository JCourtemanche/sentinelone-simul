import random
from flask import Blueprint, request, jsonify
from auth import require_api_token
from generators.alerts import generate_uam_alert
from generators.base import s1_uuid, random_count

uam_bp = Blueprint('uam', __name__)


@uam_bp.route('/web/api/v<version>/unifiedalerts/graphql', methods=['POST'])
@require_api_token
def uam_graphql(version):
    body = request.get_json() or {}
    query = body.get('query', '')
    variables = body.get('variables', {})

    # Detect query type and return appropriate response
    if 'mutation' in query.lower():
        # Mutation: update status or analyst verdict
        alert_id = variables.get('id', s1_uuid())
        status = variables.get('status')
        verdict = variables.get('verdict')

        action_result = {
            'actionId': random.choice(['S1/alert/statusUpdate', 'S1/alert/analystVerdictUpdate']),
            'alertCount': 1,
            'success': [{'id': alert_id}],
            'failure': [],
            'skip': [],
        }
        return jsonify({
            'data': {
                'alertTriggerActions': {
                    '__typename': 'ActionsTriggered',
                    'actions': [action_result],
                }
            }
        }), 200

    elif 'alert(' in query:
        # Single alert by ID
        alert_id = variables.get('id', s1_uuid())
        uam_alert = generate_uam_alert(alert_id=alert_id)
        return jsonify({'data': {'alert': uam_alert['node']}}), 200

    else:
        # List alerts query
        count = random_count(3, 10)
        edges = [generate_uam_alert() for _ in range(count)]
        has_next = random.choice([True, False])
        end_cursor = s1_uuid() if has_next else None
        return jsonify({
            'data': {
                'alerts': {
                    'edges': edges,
                    'pageInfo': {
                        'hasNextPage': has_next,
                        'hasPreviousPage': False,
                        'startCursor': s1_uuid(),
                        'endCursor': end_cursor,
                    },
                }
            }
        }), 200
