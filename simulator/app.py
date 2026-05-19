import logging
from flask import Flask, jsonify
from config import Config

from routes.agents import agents_bp
from routes.threats import threats_bp
from routes.activities import activities_bp
from routes.sites import sites_bp
from routes.groups import groups_bp
from routes.exclusions import exclusions_bp
from routes.restrictions import restrictions_bp
from routes.hashes import hashes_bp
from routes.dv import dv_bp
from routes.alerts import alerts_bp
from routes.star import star_bp
from routes.iocs import iocs_bp
from routes.accounts import accounts_bp
from routes.remote_scripts import remote_scripts_bp
from routes.uam import uam_bp
from routes.misc import misc_bp


def create_app():
    app = Flask(__name__)

    logging.basicConfig(
        level=logging.INFO if Config.DEBUG else logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    logger = logging.getLogger(__name__)
    logger.info('Starting SentinelOne API Simulator')

    blueprints = [
        agents_bp, threats_bp, activities_bp, sites_bp, groups_bp,
        exclusions_bp, restrictions_bp, hashes_bp, dv_bp, alerts_bp,
        star_bp, iocs_bp, accounts_bp, remote_scripts_bp, uam_bp, misc_bp,
    ]
    for bp in blueprints:
        app.register_blueprint(bp)

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy', 'service': 'SentinelOne API Simulator', 'version': '1.0.0'}), 200

    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'service': 'SentinelOne API Simulator',
            'version': '1.0.0',
            'description': 'Simulates SentinelOne Management API for XSIAM demo purposes',
            'authentication': 'Authorization: ApiToken <token>',
            'default_token': Config.API_TOKEN,
            'base_path': '/web/api/v2.1/',
            'endpoints': {
                'agents': 'GET /web/api/v2.1/agents',
                'threats': 'GET /web/api/v2.1/threats',
                'alerts': 'GET /web/api/v2.1/cloud-detection/alerts',
                'activities': 'GET /web/api/v2.1/activities',
                'sites': 'GET /web/api/v2.1/sites',
                'groups': 'GET /web/api/v2.1/groups',
                'iocs': 'GET /web/api/v2.1/threat-intelligence/iocs',
                'dv': 'POST /web/api/v2.1/dv/init-query',
            },
        }), 200

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'errors': [{'code': 4040010, 'detail': 'Resource not found', 'title': 'Not Found'}]}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logging.getLogger(__name__).error(f'Internal error: {error}')
        return jsonify({'errors': [{'code': 5000010, 'detail': 'Internal server error', 'title': 'Server Error'}]}), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
