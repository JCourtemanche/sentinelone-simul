import os


class Config:
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 8080))

    API_TOKEN = os.environ.get('API_TOKEN', 'test-api-token-sentinelone')

    MIN_ITEMS = int(os.environ.get('MIN_ITEMS', 1))
    MAX_ITEMS = int(os.environ.get('MAX_ITEMS', 10))

    # Stable fake site/account/group IDs reused across responses
    SITE_IDS = [
        '111111111111111111',
        '222222222222222222',
        '333333333333333333',
    ]
    ACCOUNT_IDS = [
        '999999999999999999',
    ]
    GROUP_IDS = [
        '444444444444444444',
        '555555555555555555',
    ]
