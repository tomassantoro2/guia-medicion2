"""Event record shape for session state and Excel export."""

from typing import Any, Dict, List, Optional

# Bump when Excel/metadata contract changes (see DOCUMENTATION.md).
EXPORT_FORMAT_VERSION = "2.1"


def default_event_metadata() -> Dict[str, str]:
    return {
        "page_url": "",
        "environment": "",
        "notes": "",
        "ga4_event_name": "",
    }


def normalize_event_record(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure optional metadata keys exist for backward compatibility."""
    meta = default_event_metadata()
    for k in meta:
        if k in raw and raw[k] is not None:
            meta[k] = str(raw[k])
    out = {**raw, **meta}
    return out


def empty_events_list() -> List[Dict[str, Any]]:
    return []
