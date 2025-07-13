# executors/__init__.py

from .sftp_collector import SFTPMediationCollector
from .file_validator import FileValidator

NODE_EXECUTION_MAP = {
    "SFTP Collector": SFTPMediationCollector,
    "File Validator": FileValidator,
    # Add more as needed
}
