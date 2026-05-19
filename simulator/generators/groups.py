import random
from generators.base import s1_id, s1_timestamp
from config import Config

GROUP_NAMES = ['Workstations', 'Servers', 'Laptops', 'Executives', 'DevOps']


def generate_group(group_id=None, idx=0):
    _id = group_id or (Config.GROUP_IDS[idx] if idx < len(Config.GROUP_IDS) else s1_id())
    name = GROUP_NAMES[idx % len(GROUP_NAMES)]
    site_id = Config.SITE_IDS[idx % len(Config.SITE_IDS)]
    return {
        'id': _id,
        'name': name,
        'type': random.choice(['static', 'dynamic']),
        'rank': idx + 1,
        'siteId': site_id,
        'isDefault': idx == 0,
        'creatorId': s1_id(),
        'creator': 'admin@acme.com',
        'totalAgents': random.randint(10, 200),
        'filterName': None,
        'filterId': None,
        'inherits': True,
        'registrationToken': 'eyJiQWxpYXMiOiJkZW1vLWdyb3VwIn0=',
        'policyRevision': random.randint(1, 10),
        'createdAt': s1_timestamp(days_back=400),
        'updatedAt': s1_timestamp(days_back=30),
    }


def generate_all_groups():
    return [generate_group(group_id=Config.GROUP_IDS[i], idx=i) for i in range(len(Config.GROUP_IDS))]
