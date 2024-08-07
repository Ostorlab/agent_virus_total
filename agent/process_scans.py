"""Processing scans returned by the Virus Total Public API."""

from typing import Any


from agent import markdown

# These are tools used by VirusTotal to scan files that report a big
# number of false positives, as a consequence their reports are excluded.
EXCLUDED_SCANNERS = ["K7GW", "TrendMicro-HouseCall"]


def get_technical_details(
    scans: dict[str, Any], target: str | None, scans_link: str | None
) -> str:
    """Returns a markdown table of the technical report of the scan.
    Each row presents an antivirus with corresponding scan result : Malicious/Safe.

    Args:
        scans : Dictionary of the scans.
        target : target to scan.
        scans_link : Link to the scan report.

    Returns:
        technical_detail : Markdown table of the scans results.
    """
    formatted_scans = markdown.prepare_data_for_markdown_formatting(scans)
    technical_detail = ""
    if target is not None:
        technical_detail = f"Analysis of the target `{target}`:\n"
    technical_detail += markdown.table_markdown(formatted_scans)
    if scans_link is not None:
        technical_detail += (
            f"\nFor more details, visit the [scan report]({scans_link})."
        )
    return technical_detail


def is_scan_malicious(scans: dict[str, Any]) -> bool:
    """Checks if any scanner reports the target as malicious.
    Args:
        scans : Dictionary of the scans.

    Returns:
        is_malicious : True if the target is reported as malicious false otherwise.
    """
    for scan_result in scans.values():
        if scan_result["detected"] is True:
            return True

    return False


def exclude_unreliable_scans(scans: dict[str, Any]) -> dict[str, Any]:
    """Excludes unreliable reports from the scans.

    Args:
        scans : Dictionary of the scans.

    Returns:
        scans: Dictionary of the scans with only reliable reports.
    """
    for scanner in EXCLUDED_SCANNERS:
        scans.pop(scanner, None)

    return scans
