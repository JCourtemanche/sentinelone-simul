import random
from generators.base import (
    s1_id, s1_uuid, s1_timestamp, sha256, public_ip, private_ip, mac_address,
    fake, OS_NAMES, OS_TYPES, DOMAINS, SITE_NAMES, GROUP_NAMES,
)
from xsiam_shared import USERS, COMPANY_NAME, DOMAIN
from config import Config


def generate_agent(agent_id=None, site_id=None, group_id=None, account_id=None, persona=None):
    """
    Generate a SentinelOne agent record.

    If `persona` is given (a dict from xsiam_shared.USERS), the agent uses
    that persona's hostname, OS, and internal IP.  Otherwise a random persona
    is picked from the shared list so every agent maps to a known Business Corp user.
    """
    p = persona or random.choice(USERS)
    os_type = p["os_type"]
    os_name = p["os_name"]

    _site_id = site_id or random.choice(Config.SITE_IDS)
    _group_id = group_id or random.choice(Config.GROUP_IDS)
    _account_id = account_id or Config.ACCOUNT_IDS[0]

    return {
        'id': agent_id or s1_id(),
        'uuid': s1_uuid(),
        'computerName': p["hostname"],
        'osName': os_name,
        'osType': os_type,
        'osRevision': fake.numerify('##H#'),
        'agentVersion': random.choice(['23.4.2.14', '23.3.1.10', '22.3.4.16']),
        'isActive': random.choice([True, True, True, False]),
        'isDecommissioned': random.choice([False, False, False, True]),
        'networkStatus': random.choice(['connected', 'connected', 'disconnected']),
        'lastActiveDate': s1_timestamp(days_back=7),
        'registeredAt': s1_timestamp(days_back=365),
        'createdAt': s1_timestamp(days_back=365),
        'updatedAt': s1_timestamp(days_back=30),
        'externalIp': public_ip(),
        'localIp': p["internal_ip"],
        'activeThreats': random.randint(0, 5),
        'encryptedApplications': random.choice([True, False]),
        'machineType': p["machine_type"],
        'domain': DOMAIN,
        'siteId': _site_id,
        'siteName': random.choice(SITE_NAMES),
        'groupId': _group_id,
        'groupName': random.choice(GROUP_NAMES),
        'accountId': _account_id,
        'accountName': COMPANY_NAME,
        'totalMemory': random.choice([4096, 8192, 16384, 32768]),
        'cpuId': random.choice(['Intel Core i7-10700', 'Intel Xeon E5-2680', 'AMD Ryzen 7 5800X']),
        'modelName': random.choice(['Dell OptiPlex 7090', 'HP EliteBook 840', 'Lenovo ThinkPad X1']),
        'serialNumber': fake.bothify('??###??###'),
        'mitigationMode': random.choice(['protect', 'detect']),
        'mitigationModeSuspicious': random.choice(['protect', 'detect']),
        'scanStatus': random.choice(['none', 'finished', 'started']),
        'networkInterfaces': [
            {
                'id': s1_id(),
                'name': random.choice(['eth0', 'en0', 'Ethernet']),
                'inet': [p["internal_ip"]],
                'inet6': [],
                'physical': mac_address(),
            }
        ],
        'tags': {'sentinelone': []},
    }


def generate_agent_process(agent_id):
    persona = random.choice(USERS)
    return {
        'pid': random.randint(1000, 65535),
        'processName': random.choice([
            'chrome.exe', 'svchost.exe', 'explorer.exe', 'python.exe',
            'node.exe', 'outlook.exe', 'teams.exe', 'powershell.exe',
        ]),
        'user': persona["username"],
        'startTime': s1_timestamp(days_back=1),
        'cpuUsage': round(random.uniform(0, 50), 2),
        'memoryUsage': random.randint(10, 500),
        'publisherName': random.choice(['Microsoft Corporation', 'Google LLC', 'Mozilla', '']),
        'sha1': None,
        'absolutePath': random.choice([
            'C:\\Windows\\System32\\svchost.exe',
            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            '/usr/bin/python3',
        ]),
    }


def generate_installed_application():
    return {
        'name': random.choice([
            'Microsoft Office 365', 'Google Chrome', 'Mozilla Firefox',
            'Adobe Acrobat Reader', 'Zoom', 'Slack', '7-Zip', 'Python 3.11',
        ]),
        'version': fake.numerify('#.#.####'),
        'publisher': random.choice(['Microsoft', 'Google LLC', 'Mozilla', 'Adobe', 'Zoom', 'Slack', '']),
        'installedDate': s1_timestamp(days_back=200),
        'size': random.randint(1024, 500000),
    }
