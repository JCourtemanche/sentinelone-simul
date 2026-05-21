import uuid
import random
import hashlib
from datetime import datetime, timedelta
from faker import Faker
from xsiam_shared import USERS, INTERNAL_IPS, MALICIOUS_IPS, DOMAIN, COMPANY_NAME

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
    """Return a Business Corp internal IP (192.168.1.x)."""
    return random.choice(INTERNAL_IPS)


def malicious_ip():
    """Return one of the shared malicious IPs."""
    return random.choice(MALICIOUS_IPS)


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


# Persona-derived lists for use throughout generators
COMPUTER_NAMES = [u["hostname"] for u in USERS]
OS_NAMES = list({u["os_name"] for u in USERS})
OS_TYPES = list({u["os_type"] for u in USERS})

DOMAINS = [DOMAIN, f'corp.{DOMAIN}', f'internal.{DOMAIN}']

SITE_NAMES = ['HQ', 'Branch-Paris', 'Branch-London', 'DataCenter-EU', 'Cloud-Prod']

GROUP_NAMES = ['Workstations', 'Servers', 'Laptops', 'Executives', 'DevOps']
