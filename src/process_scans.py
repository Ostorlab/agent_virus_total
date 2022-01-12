"""Processing scans returned by the Virus Total Public API."""
from typing import Dict

from . import markdown


def get_risk_rating(scans:Dict) -> str:
    """Assign risk level based on scanned file report.
    Returns:
        'HIGH' if at least one anti-virus detected the file as a virus, else Secure.
    """
    for scanner_result in scans.values():
        if scanner_result['detected']:
            return 'HIGH'
    return 'SECURE'

def get_technical_details(scans:Dict) -> str:
    """Returns a markdwon table of the technical report of the scan.
    Each row presents an antivirus with corresponding scan result : Malicious/Safe.
    Args:
        scans : Dictionary of the scans.
    Returns:
        technical_detail : Markdown table of the scans results.
    """
    scans = markdown.prepare_data_for_markdown_formatting(scans)
    technical_detail = markdown.table_markdown(scans)
    return technical_detail
