import random
from generators.base import s1_id, s1_timestamp, fake
from config import Config

ACTIVITY_TYPES = [
    (2010, 'Agent logged in to Management Console'),
    (2012, 'Agent policy updated'),
    (3001, 'Threat detected'),
    (3002, 'Threat quarantined'),
    (3003, 'Threat remediated'),
    (3005, 'Threat resolved'),
    (3013, 'Threat marked as benign'),
    (4001, 'Agent connected'),
    (4002, 'Agent disconnected'),
    (4006, 'Agent uninstalled'),
    (5001, 'Hash blocked'),
    (5002, 'Hash unblocked'),
    (6001, 'Exclusion created'),
    (6002, 'Exclusion deleted'),
]


def generate_activity(activity_id=None):
    act_type, description = random.choice(ACTIVITY_TYPES)
    _site_id = random.choice(Config.SITE_IDS)
    agent_id = s1_id()

    return {
        'id': activity_id or s1_id(),
        'activityType': act_type,
        'createdAt': s1_timestamp(days_back=30),
        'updatedAt': s1_timestamp(days_back=7),
        'primaryDescription': description,
        'secondaryDescription': fake.sentence(nb_words=8),
        'agentId': agent_id,
        'agentUpdatedVersion': None,
        'comments': None,
        'data': {
            'accountName': 'Acme Corp',
            'computerName': 'DESKTOP-' + fake.lexify('????????').upper(),
            'groupName': random.choice(['Workstations', 'Servers', 'Laptops']),
            'role': 'Admin',
            'siteName': random.choice(['HQ', 'Branch-Paris', 'DataCenter-EU']),
            'username': fake.email(),
        },
        'groupId': random.choice(Config.GROUP_IDS),
        'hash': None,
        'osFamily': random.choice(['windows', 'macos', 'linux']),
        'siteId': _site_id,
        'threatId': s1_id() if act_type in (3001, 3002, 3003, 3005, 3013) else None,
        'userId': s1_id(),
    }
