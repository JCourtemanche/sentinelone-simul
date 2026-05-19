import random
from generators.base import (
    s1_id, s1_uuid, s1_timestamp, sha1, sha256,
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

# Valeurs exactes attendues par le filtre fetch_severity de l'intégration
SEVERITIES = ['Low', 'Medium', 'High', 'Critical']
INCIDENT_STATUSES = ['UNRESOLVED', 'IN_PROGRESS', 'RESOLVED']
ANALYST_VERDICTS = ['UNDEFINED', 'TRUE_POSITIVE', 'FALSE_POSITIVE', 'SUSPICIOUS']
EVENT_TYPES = ['Process Creation', 'Network Connection', 'File Creation', 'Registry Key Set', 'DNS Query']


def _process_info():
    return {
        'name': random.choice(['powershell.exe', 'cmd.exe', 'python.exe', 'bash', 'wscript.exe']),
        'filePath': random.choice([
            'C:\\Windows\\System32\\powershell.exe',
            'C:\\Windows\\System32\\cmd.exe',
            '/usr/bin/python3',
            '/bin/bash',
        ]),
        'commandline': fake.sentence(nb_words=8),
        'user': fake.user_name(),
        'fileHashSha1': sha1(),
        'fileHashSha256': sha256(),
        'pidStarttime': s1_timestamp(days_back=1),
        'storyline': s1_uuid(),
        'fileSignerIdentity': random.choice(['Microsoft Corporation', 'Google LLC', '', None]),
    }


def generate_alert(alert_id=None):
    os_type = random.choice(OS_TYPES)
    agent_id = s1_id()
    agent_uuid = s1_uuid()
    _site_id = random.choice(Config.SITE_IDS)
    _site_name = random.choice(SITE_NAMES)
    _group_id = random.choice(Config.GROUP_IDS)
    alert_name = random.choice(ALERT_NAMES)
    severity = random.choice(SEVERITIES)
    rule_id = s1_id()
    alert_internal_id = alert_id or s1_id()
    created_at = s1_timestamp(days_back=30)

    return {
        'id': alert_internal_id,

        # Champ critique pour fetch-incidents : ruleInfo.severity et ruleInfo.name
        'ruleInfo': {
            'id': rule_id,
            'name': alert_name,
            'severity': severity,
            'treatAsThreat': random.choice(['Malicious', 'Suspicious', 'UNDEFINED']),
            'description': fake.sentence(nb_words=12),
            'queryType': random.choice(['events', 'processes']),
            'scopeLevel': 'account',
            'scopeName': 'Acme Corp',
        },

        # Champ critique pour to_incident : alertInfo.createdAt
        'alertInfo': {
            'alertId': alert_internal_id,
            'eventType': random.choice(EVENT_TYPES),
            'createdAt': created_at,
            'updatedAt': s1_timestamp(days_back=7),
            'incidentStatus': random.choice(INCIDENT_STATUSES),
            'analystVerdict': random.choice(ANALYST_VERDICTS),
            'dvEventId': s1_uuid(),
            'hitType': 'Events',
            'source': random.choice(['STAR', 'CLOUD', 'ENDPOINT']),
            'reportedAt': created_at,
        },

        # Champ accédé dans get_alerts_command
        'agentRealtimeInfo': {
            'id': agent_id,
            'name': 'DESKTOP-' + fake.lexify('????????').upper(),
            'os': os_type,
            'agentVersion': '23.4.2.14',
            'networkStatus': 'connected',
            'mitigationMode': 'protect',
            'operationalState': 'na',
            'activeThreats': random.randint(0, 3),
        },

        'agentDetectionInfo': {
            'agentId': agent_id,
            'uuid': agent_uuid,
            'agentComputerName': 'DESKTOP-' + fake.lexify('????????').upper(),
            'siteId': _site_id,
            'siteName': _site_name,
            'version': '23.4.2.14',
            'agentOsType': os_type,
            'agentOsName': 'Windows 10 Pro' if os_type == 'windows' else 'Ubuntu 22.04',
            'groupId': _group_id,
            'groupName': random.choice(['Workstations', 'Servers']),
            'accountId': Config.ACCOUNT_IDS[0],
            'accountName': 'Acme Corp',
        },

        'sourceProcessInfo': _process_info(),
        'sourceParentProcessInfo': _process_info(),

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
    }


def generate_uam_alert(alert_id=None):
    """UAM alert retourné par GraphQL."""
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
            'result': random.choice(['Malicious', 'Suspicious', None]),
            'classification': random.choice(['Malware', 'PUA', 'Ransomware', None]),
            'confidenceLevel': random.choice(['malicious', 'suspicious', 'n/a']),
            'externalId': None,
            'firstSeenAt': s1_timestamp(days_back=30),
            'lastSeenAt': s1_timestamp(days_back=1),
            'detectedAt': s1_timestamp(days_back=30),
            'noteExists': False,
            'dataSources': [],
            'storylineId': s1_uuid(),
            'ticketId': None,
            'fileName': None,
            'fileHash': None,
            'analytics': None,
            'assignee': None,
            'asset': {
                'agentUuid': s1_uuid(),
                'osType': random.choice(OS_TYPES),
                'osVersion': 'Windows 10 Pro',
                'agentVersion': '23.4.2.14',
            },
            'realTime': {
                'scope': {
                    'account': {
                        'id': Config.ACCOUNT_IDS[0],
                        'name': 'Acme Corp',
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
            },
            'detectionTime': {
                'cloud': None,
                'kubernetes': None,
            },
        }
    }
