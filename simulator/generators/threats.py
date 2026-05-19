import random
from generators.base import (
    s1_id, s1_uuid, s1_timestamp, sha1, sha256, md5,
    fake, OS_TYPES, SITE_NAMES,
)
from config import Config

THREAT_NAMES = [
    'Exploit.Win32.CVE-2021-40444',
    'Trojan.Ransom.LockBit',
    'Backdoor.Python.Agent',
    'Malware.Mimikatz',
    'PUA.Win32.CoinMiner',
    'Trojan.GenericKD.46125',
    'Exploit.Shellcode.Generic',
    'Ransomware.WannaCry',
    'Spyware.Formbook',
    'Trojan.Emotet',
]

CLASSIFICATIONS = ['Malware', 'PUA', 'Ransomware', 'Trojan', 'Exploit', 'Adware']
MITIGATION_STATUSES = ['mitigated', 'active', 'blocked', 'suspicious', 'pending']
CONFIDENCE_LEVELS = ['malicious', 'suspicious', 'n/a']
ANALYST_VERDICTS = ['true_positive', 'false_positive', 'suspicious', 'undefined']
INCIDENT_STATUSES = ['unresolved', 'in_progress', 'resolved']


def generate_threat(threat_id=None):
    os_type = random.choice(OS_TYPES)
    _site_id = random.choice(Config.SITE_IDS)
    agent_id = s1_id()

    file_path = random.choice([
        'C:\\Users\\{}\\AppData\\Local\\Temp\\'.format(fake.user_name()),
        'C:\\Windows\\Temp\\',
        '/tmp/',
        '/var/tmp/',
        '/home/{}/Downloads/'.format(fake.user_name()),
    ])
    file_name = fake.file_name(extension=random.choice(['exe', 'dll', 'ps1', 'sh', 'py']))

    return {
        'id': threat_id or s1_id(),
        'threatInfo': {
            'createdAt': s1_timestamp(days_back=30),
            'updatedAt': s1_timestamp(days_back=7),
            'classification': random.choice(CLASSIFICATIONS),
            'classificationSource': random.choice(['Cloud', 'Engine', 'Static']),
            'mitigationStatus': random.choice(MITIGATION_STATUSES),
            'confidenceLevel': random.choice(CONFIDENCE_LEVELS),
            'sha1': sha1(),
            'sha256': sha256(),
            'md5': md5(),
            'threatName': random.choice(THREAT_NAMES),
            'filePath': file_path + file_name,
            'fileDisplayName': file_name,
            'processUser': fake.user_name(),
            'analystVerdict': random.choice(ANALYST_VERDICTS),
            'incidentStatus': random.choice(INCIDENT_STATUSES),
            'initiatedBy': random.choice(['agent_policy', 'user', 'cloud']),
            'initiatedByDescription': 'Policy',
            'reachedEventsLimit': False,
            'pendingActions': False,
            'engines': [random.choice(['DBT', 'reputation', 'pre_execution', 'intrusion_detection'])],
        },
        'agentRealtimeInfo': {
            'agentId': agent_id,
            'agentComputerName': 'DESKTOP-' + fake.lexify('????????').upper(),
            'siteId': _site_id,
            'siteName': random.choice(SITE_NAMES),
            'agentOsType': os_type,
            'agentVersion': random.choice(['23.4.2.14', '23.3.1.10']),
            'agentMitigationMode': random.choice(['protect', 'detect']),
            'networkStatus': random.choice(['connected', 'disconnected']),
            'operationalState': 'na',
            'groupId': random.choice(Config.GROUP_IDS),
            'groupName': random.choice(['Workstations', 'Servers', 'Laptops']),
            'accountId': Config.ACCOUNT_IDS[0],
            'accountName': 'Acme Corp',
        },
        'containerInfo': None,
        'kubernetesInfo': None,
        'indicators': [],
        'mitigationStatus': [
            {
                'action': random.choice(['quarantine', 'kill', 'remediate']),
                'actionsCounters': {'failed': 0, 'notFound': 0, 'pendingReboot': 0, 'success': 1, 'total': 1},
                'agentSupportsReport': True,
                'groupNotFound': False,
                'lastUpdate': s1_timestamp(days_back=7),
                'latestReport': '',
                'mitigation_ended_at': s1_timestamp(days_back=7),
                'mitigation_started_at': s1_timestamp(days_back=7),
                'status': 'success',
            }
        ],
        'whiteningOptions': [],
    }


def generate_threat_note(threat_id, note_id=None):
    return {
        'id': note_id or s1_id(),
        'threatId': threat_id,
        'text': random.choice([
            'Investigated - confirmed malware, contained.',
            'False positive - internal tool flagged.',
            'Under investigation by SOC team.',
            'Escalated to Tier 2.',
        ]),
        'createdAt': s1_timestamp(days_back=10),
        'updatedAt': s1_timestamp(days_back=5),
        'creator': fake.name(),
        'creatorId': s1_id(),
    }


def generate_threat_summary():
    return {
        'data': {
            'threats': {
                'notMitigated': random.randint(0, 5),
                'notMitigatedNotResolved': random.randint(0, 3),
                'notResolved': random.randint(0, 8),
                'total': random.randint(10, 100),
            },
            'statistics': {
                'critical': random.randint(0, 2),
                'high': random.randint(0, 10),
                'medium': random.randint(0, 20),
                'low': random.randint(0, 50),
            },
        },
        'errors': None,
    }


def generate_threat_analysis(threat_id):
    return {
        'data': {
            'id': threat_id,
            'threatId': threat_id,
            'overview': {
                'fullPath': '/tmp/malware.exe',
                'md5': md5(),
                'sha1': sha1(),
                'sha256': sha256(),
                'fileSize': random.randint(10000, 5000000),
            },
            'network': {
                'connections': [
                    {
                        'remoteAddress': fake.ipv4_public(),
                        'remotePort': random.choice([80, 443, 8080, 4444]),
                        'protocol': 'TCP',
                    }
                ]
            },
            'indicators': [
                {'category': 'Network', 'description': 'Suspicious outbound connection'},
                {'category': 'File', 'description': 'Dropped executable in temp directory'},
            ],
        },
        'errors': None,
    }
