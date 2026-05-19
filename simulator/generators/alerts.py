import random
from generators.base import (
    s1_id, s1_uuid, s1_timestamp, sha256,
    fake, OS_TYPES, SITE_NAMES,
)
from config import Config

ALERT_NAMES = [
    'Lateral Movement - Pass the Hash',
    'Credential Dumping via LSASS',
    'Suspicious PowerShell Execution',
    'Ransomware Behavior Detected',
    'Data Exfiltration via DNS',
    'Process Injection Detected',
    'Privilege Escalation Attempt',
    'Suspicious Network Scan',
    'Malicious Script Execution',
    'Command and Control Communication',
]

SEVERITIES = ['Low', 'Medium', 'High', 'Critical']
INCIDENT_STATUSES = ['UNRESOLVED', 'IN_PROGRESS', 'RESOLVED']
ANALYST_VERDICTS = ['UNDEFINED', 'TRUE_POSITIVE', 'FALSE_POSITIVE', 'SUSPICIOUS']


def generate_alert(alert_id=None):
    os_type = random.choice(OS_TYPES)
    agent_id = s1_id()
    _site_id = random.choice(Config.SITE_IDS)

    return {
        'id': alert_id or s1_id(),
        'alertInfo': {
            'alertName': random.choice(ALERT_NAMES),
            'severity': random.choice(SEVERITIES),
            'createdAt': s1_timestamp(days_back=30),
            'updatedAt': s1_timestamp(days_back=7),
            'incidentStatus': random.choice(INCIDENT_STATUSES),
            'analystVerdict': random.choice(ANALYST_VERDICTS),
            'alertState': random.choice(['ACTIVE', 'DISMISSED']),
            'reportedAt': s1_timestamp(days_back=30),
            'source': random.choice(['STAR', 'CLOUD', 'ENDPOINT']),
            'hitType': 'Events',
            'eventType': random.choice(['PROCESS', 'NETWORK', 'FILE', 'REGISTRY']),
            'ruleId': s1_id(),
            'ruleName': random.choice(['Custom STAR Rule', 'Built-in Detection']),
            'dvEventId': s1_uuid(),
        },
        'agentDetectionInfo': {
            'agentId': agent_id,
            'agentComputerName': 'DESKTOP-' + fake.lexify('????????').upper(),
            'siteId': _site_id,
            'siteName': random.choice(SITE_NAMES),
            'agentOsType': os_type,
            'agentOsName': 'Windows 10 Pro' if os_type == 'windows' else 'Ubuntu 22.04',
            'agentVersion': '23.4.2.14',
            'groupId': random.choice(Config.GROUP_IDS),
            'groupName': random.choice(['Workstations', 'Servers']),
            'accountId': Config.ACCOUNT_IDS[0],
            'accountName': 'Acme Corp',
            'agentUuid': s1_uuid(),
        },
        'agentRealtimeInfo': {
            'agentId': agent_id,
            'agentComputerName': 'DESKTOP-' + fake.lexify('????????').upper(),
            'networkStatus': 'connected',
            'agentMitigationMode': 'protect',
            'operationalState': 'na',
        },
        'containerInfo': {
            'id': None,
            'name': None,
            'image': None,
            'isContainerQuarantine': False,
        },
        'indicators': [
            {
                'ids': [random.randint(1, 200)],
                'category': random.choice(['General', 'Persistence', 'Lateral Movement']),
                'description': 'Indicator of compromise detected',
            }
        ],
        'sourceProcessInfo': {
            'pid': random.randint(1000, 65535),
            'name': random.choice(['powershell.exe', 'cmd.exe', 'python.exe', 'bash']),
            'filePath': random.choice([
                'C:\\Windows\\System32\\powershell.exe',
                '/usr/bin/python3',
            ]),
            'commandLine': fake.sentence(nb_words=8),
            'user': fake.user_name(),
            'sha256': sha256(),
            'startTime': s1_timestamp(days_back=1),
        },
        'targetProcessInfo': None,
    }


def generate_uam_alert(alert_id=None):
    """UAM alert returned from GraphQL."""
    _id = alert_id or s1_uuid()
    return {
        'node': {
            'id': _id,
            'name': random.choice(ALERT_NAMES),
            'severity': random.choice(['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']),
            'status': random.choice(['New', 'In progress', 'Resolved']),
            'analystVerdict': random.choice([
                'Undefined',
                'True positive - Malware',
                'False positive - Benign',
            ]),
            'createdAt': s1_timestamp(days_back=30),
            'updatedAt': s1_timestamp(days_back=7),
            'description': fake.sentence(nb_words=12),
            'source': random.choice(['CLOUD', 'ENDPOINT', 'IDENTITY']),
            'agent': {
                'id': s1_id(),
                'computerName': 'DESKTOP-' + fake.lexify('????????').upper(),
            },
            'group': {
                'id': random.choice(Config.GROUP_IDS),
                'name': random.choice(['Workstations', 'Servers']),
            },
            'site': {
                'id': random.choice(Config.SITE_IDS),
                'name': random.choice(SITE_NAMES),
            },
        }
    }
