import random
from generators.base import s1_id, s1_timestamp
from config import Config

SITE_NAMES = ['HQ', 'Branch-Paris', 'Branch-London', 'DataCenter-EU', 'Cloud-Prod']


def generate_site(site_id=None, idx=0):
    _id = site_id or (Config.SITE_IDS[idx] if idx < len(Config.SITE_IDS) else s1_id())
    name = SITE_NAMES[idx % len(SITE_NAMES)]
    return {
        'id': _id,
        'name': name,
        'accountId': Config.ACCOUNT_IDS[0],
        'accountName': 'Acme Corp',
        'activeLicenses': random.randint(10, 500),
        'totalLicenses': random.randint(500, 1000),
        'creator': 'admin@acme.com',
        'creatorId': s1_id(),
        'description': f'Site for {name}',
        'expiration': None,
        'externalId': None,
        'healthStatus': True,
        'isDefault': idx == 0,
        'registrationToken': 'eyJiQWxpYXMiOiJkZW1vIn0=',
        'siteType': 'Paid',
        'state': 'active',
        'totalAgents': random.randint(50, 500),
        'activeAgents': random.randint(40, 490),
        'unlimitedExpiration': True,
        'unlimitedLicenses': False,
        'createdAt': s1_timestamp(days_back=500),
        'updatedAt': s1_timestamp(days_back=30),
        'licenses': {
            'bundles': [
                {
                    'name': 'Complete',
                    'surfaces': [
                        {'name': 'Endpoint', 'totalLicenses': random.randint(500, 1000), 'usedLicenses': random.randint(10, 500)},
                    ],
                }
            ]
        },
    }


def generate_all_sites():
    return [generate_site(site_id=Config.SITE_IDS[i], idx=i) for i in range(len(Config.SITE_IDS))]
