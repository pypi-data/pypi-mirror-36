# Copyright (c) 2018 UniquID

"""Constant definitions."""

# application version number
APP_VERSION = '0.4.2'

# minimum supported version of python
MIN_VERSION_MAJOR = 3
MIN_VERSION_MINOR = 6

# maximum supported version of credentials file
MAX_VERSION_CREDENTIALS = 1

# permanent Uniquid HTTP API address
# see COR-330: IP address and Port Number of Onboarding HTTP API.
# static file server
UNIQUID_STATIC_IP = '52.47.161.93'
UNIQUID_STATIC_PORT = '80'
# onboarding server
UNIQUID_LOGIN_IP = '52.47.97.110'
UNIQUID_LOGIN_PORT = '3000'
UNIQUID_URL_SCHEME = 'http://'
ORCHESTRATOR_PORT = '8080'

# supported IoT PaaS platforms. used by deploy command.
PLATFORMS = ['aws']
# AWS security group ports
AWS_SEC_GROUP_PORTS = ['22', '8070']
# path to static file containing AWS Agent package
AWS_AGENT_URL_PATH = '/static/awsagent/latest.tar.gz'

# error messages for authentication and login
ERR_LOGGED_OUT = 'User is logged out. Please login again.'
ERR_LOGIN_REJECTED = 'Login rejected. Please check user credentials.'
ERR_LOGOUT_REJECTED = 'Logout rejected. Session may have expired.'
ERR_LOGOUT_ERROR = 'Failed to logout. May already be logged out.'
ERR_ORG_NOT_FOUND = 'Organization not registered at Uniquid: '
ERR_QUERY_ERROR = 'Server returned bad data.'
ERR_MISSING_API_KEY = 'Login fail. Missing API key.'
ERR_MISSING_USERNAME = 'Login fail. Missing Username or email.'
ERR_MISSING_ORG_ID = 'Login fail. Missing Organization ID.'
ERR_MISSING_ORG_PORT = 'Login fail. Missing Organization IP/port.'
ERR_CRED_ORG = 'Login fail. Cannot specify credential file and organization.'
ERR_CRED_USER = 'Login fail. Cannot specify credential file and user.'
ERR_CRED_KEY = 'Login fail. Cannot specify credential file and access key.'
ERR_ORG_ID_URL = 'Login fail. Cannot specify organization identifier and URL.'
ERR_LOGIN_ORG_URL = 'Login fail. Specified login URL and organization URL.'
ERR_BAD_ORCH_URL = 'Login fail. Incorrect API URL.'
ERR_MISSING_IP_PORT = 'Login fail. Require both HTTP API IP and port number.'
ERR_NO_RESPONSE = 'Connection fail. No response from server.'
ERR_INVALID_URL = 'Login fail. Invalid Uniquid URL as argument.'
ERR_ORCHESTRATOR_SPINUP = 'Login suspended.'
ERR_FILE_PERM = "Insufficient permissions to open file: "
ERR_FILE_OPEN = "Login fail. Missing credentials file: "
ERR_ORCH_REQ_FAIL = 'Failed to retrieve properties for Organization.'
# error messages for commands
ERR_ENDPOINT_REJECTED = 'Server rejected credentials. Please login again.'
ERR_SERVER_ERROR = 'Server internal error. Please try again.'
ERR_SINGLE_OPTION = 'One option/argument must be passed.'
ERR_INVALID_JSON = 'Invalid format of JSON data.'
ERR_MISSING_TXID = 'TXID must be passed to command.'
ERR_NO_CONTRACT = 'Contract not found.'
ERR_NO_SHARE = 'Share not found. Share Id: '
ERR_BAD_PLATFORM = 'Platform not supported.'
ERR_MISSING_DEPENDENCY = 'Missing dependency. Cannot proceed.'
# error messages for file system
ERR_TEMP_FILE = ('Failed to create or access a temporary file. ' +
                 'Check directory permissions.')
ERR_BAD_CRED_FILE = 'Invalid credentials file.'
ERR_CRED_FILE_VERSION = 'Unsupported version of credentials file.'
# error messages for AWS
ERR_AWS_NOT_CONFIGURED = 'AWS CLI tool is not configured. Halting command.'
ERR_AWS_QUERY_ACCOUNT = 'AWS account identifier not retrieved.'
ERR_AWS_REPLY_MISSING_DATA = 'Missing data from reply to AWS CLI command. Missing: '
ERR_AWS_SEC_GROUP_EXISTS = 'AWS Security Group already exists.'
ERR_AWS_SEC_GROUP_NOT_EXISTS = 'AWS Security Group does not exist.'
ERR_AWS_KEYPAIR_FILE_CREATE = 'Error creating AWS EC2 key pair file: '
ERR_AWS_KEYPAIR_FILE_READ = 'Error reading AWS EC2 key pair file: '
ERR_AWS_INVALID_KEYPAIR_NAME = 'Invalid name for EC2 key pair.'
ERR_AWS_CANNOT_FIND_INSTANCE = 'Cannot find EC2 instance: '
ERR_NO_AWS_IMAGE = 'Cannot find a suitable EC2 image.'
ERR_SHELL_COMMAND_FAILED = 'Shell command returned an error.'
# unknown error - shouldn't happen
ERR_UNKNOWN_ERROR = 'Error occurred. Please try again.'

# supported formats for data output to the console
FORMAT_TEXT = 'text'
FORMAT_JSON = 'json'
FORMAT_ALL = [FORMAT_TEXT, FORMAT_JSON]

# User dialogs
TXT_TAB = '\t'
TXT_PASS = 'Done.'
TXT_PREFIX_OK = 'Success. '
TXT_PREFIX_FAIL = 'Failure. '
TXT_LOGIN_OK = TXT_PREFIX_OK + 'Logged in: '
TXT_LOGOUT_OK = TXT_PREFIX_OK + 'Logged out: '
TXT_CONTRACT_CREATED = TXT_PREFIX_OK + 'Contract(s) requested: '
TXT_CONTRACT_CREATED_ALL = TXT_PREFIX_OK + 'All contracts requested.'
TXT_CONTRACT_INTERRUPTED = (TXT_PREFIX_FAIL +
                            'Requests interrupted. Contract(s) requested: ')
TXT_CONTRACT_DELETED = TXT_PREFIX_OK + 'Contract deleted. TXID: '
TXT_CONTRACT_DELETED_ALL = TXT_PREFIX_OK + 'All contracts deleted.'
TXT_SHARE_CREATED = TXT_PREFIX_OK + 'Devices shared: '
TXT_SHARE_INTERRUPTED = (TXT_PREFIX_FAIL +
                         'Share creation interrupted. Devices shared: ')
TXT_SHARE_DEL_INTERRUPTED = (TXT_PREFIX_FAIL +
                             ('Share deletion interrupted. '
                              ' Device share(s) deleted: '))
TXT_SHARE_DELETED = TXT_PREFIX_OK + ' Share(s) deleted: '
TXT_LOGIN_FAIL_ORCH_SPINUP = (TXT_PREFIX_FAIL +
                              ('System is starting up. Please try again after '
                               'a brief wait.'))
TXT_CONN_STATUS = 'STATUS'
TXT_CONN_LOGGED_IN = 'Logged In'
TXT_CONN_LOGGED_OUT = 'Logged Out'
TXT_ORG_ID = 'ORGANIZATION'
# aws deploy dialogs
TXT_AWS_SEC_GROUP_CREATED = 'AWS Security Group created. Id: '
TXT_AWS_PORT_OPENED = 'AWS Security Group inbound TCP port opened: '
TXT_AWS_KEYPAIR_FILE_WRITTEN = 'AWS Key Pair file saved: '
TXT_AWS_EXIT_EARLY = 'User terminated deploy process.'
TXT_AWS_WAIT_INSTANCE_RUNNING = 'Waiting on EC2 instance to start running.'

# device sharing directions
SHARE_DIR_IN = 'in'
SHARE_DIR_OUT = 'out'
SHARE_DIR_BOTH = 'all'
SHARE_DIR_ALL = [SHARE_DIR_IN, SHARE_DIR_OUT, SHARE_DIR_BOTH]

# keys of JSON objects used in Orchestrator HTTP API
KEY_ORG_ID = 'orgId'

# credentials file schema
CREDENTIALS_SCHEMA = {
    'type': 'object',
    'properties': {
        'version': {'type': 'number'},
        'organization': {'type': 'string'},
        'user': {'type': 'string'},
        'accessKey': {'type': 'string'}
    },
    'required': ['version', 'organization', 'user', 'accessKey']
}
