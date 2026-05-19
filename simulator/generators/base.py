import uuid
import random
import hashlib
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()


def s1_id():
    """Generate a SentinelOne-style 18-digit numeric ID."""
    return str(random.randint(100000000000000000, 999999999999999999))


def s1_uuid():
    return str(uuid.uuid4())


def s1_timestamp(days_back=30):
    """ISO8601 timestamp within the last `days_back` days."""
    dt = fake.date_time_between(start_date=f'-{days_back}d', end_date='now')
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'


def sha1():
    return hashlib.sha1(fake.binary(length=20)).hexdigest()


def sha256():
    return hashlib.sha256(fake.binary(length=32)).hexdigest()


def md5():
    return hashlib.md5(fake.binary(length=16)).hexdigest()


def public_ip():
    return fake.ipv4_public()


def private_ip():
    return fake.ipv4_private()


def mac_address():
    return fake.mac_address()


def s1_response(data, total=None, next_cursor=None):
    """Wrap data in standard SentinelOne response envelope."""
    if total is None:
        total = len(data) if isinstance(data, list) else 1
    return {
        'data': data,
        'pagination': {
            'totalItems': total,
            'nextCursor': next_cursor,
        },
        'errors': None,
    }


def s1_affected(n=1):
    """Response for action endpoints."""
    return {'data': {'affected': n}, 'errors': None}


def random_count(min_val=None, max_val=None):
    from config import Config
    lo = min_val if min_val is not None else Config.MIN_ITEMS
    hi = max_val if max_val is not None else Config.MAX_ITEMS
    return random.randint(lo, hi)


COMPUTER_NAMES = [
    'DESKTOP-{}'.format(fake.lexify('????????').upper()),
    'LAPTOP-{}'.format(fake.lexify('??????').upper()),
    'WS-{}'.format(fake.numerify('####')),
    'SRV-{}'.format(fake.lexify('????').upper()),
]

OS_NAMES = [
    'Windows 10 Pro', 'Windows 11 Pro', 'Windows Server 2019',
    'macOS 14.0', 'macOS 13.5', 'Ubuntu 22.04 LTS', 'CentOS 7',
]

OS_TYPES = ['windows', 'macos', 'linux']

DOMAINS = ['corp.example.com', 'internal.acme.net', 'enterprise.local', 'lab.test']

SITE_NAMES = ['HQ', 'Branch-Paris', 'Branch-London', 'DataCenter-EU', 'Cloud-Prod']

GROUP_NAMES = ['Workstations', 'Servers', 'Laptops', 'Executives', 'DevOps']
