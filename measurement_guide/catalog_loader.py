"""Load catalog manifest, MTP event lists, and GA4 template definitions."""

import json
import os
from typing import Any, Dict, List, Tuple


def _base_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_manifest() -> Dict[str, Any]:
    path = os.path.join(_base_dir(), "catalogs", "manifest.json")
    if not os.path.isfile(path):
        return {"version": 1, "catalogs": [], "ga4_templates_file": "ga4_recommended.json"}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _resolve_catalog_path(filename: str) -> str:
    base = _base_dir()
    primary = os.path.join(base, "catalogs", filename)
    if os.path.isfile(primary):
        return primary
    legacy = os.path.join(base, filename)
    if os.path.isfile(legacy):
        return legacy
    return primary


def load_mtp_events_from_file(filename: str) -> List[Dict[str, Any]]:
    path = _resolve_catalog_path(filename)
    if not os.path.isfile(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def load_ga4_templates() -> List[Dict[str, Any]]:
    manifest = load_manifest()
    name = manifest.get("ga4_templates_file", "ga4_recommended.json")
    path = os.path.join(_base_dir(), "catalogs", name)
    if not os.path.isfile(path):
        path = _resolve_catalog_path(name)
    if not os.path.isfile(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "templates" in data:
            return list(data["templates"])
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []


def catalog_choices() -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Returns (catalog_entries, radio_labels) where each entry is
    {id, label, type, file} and type is 'mtp' or 'ga4_file' (unused for ga4 — templates separate).
    """
    manifest = load_manifest()
    entries: List[Dict[str, Any]] = []
    labels: List[str] = ["Custom event", "GA4 recommended template"]
    for c in manifest.get("catalogs", []):
        if c.get("type") == "mtp" and c.get("file"):
            entries.append(
                {
                    "id": c.get("id", "mtp"),
                    "label": c.get("label", "MTP catalog"),
                    "type": "mtp",
                    "file": c["file"],
                }
            )
            labels.append(c.get("label", "MTP catalog"))
    return entries, labels


def load_mtp_for_entry(entry: Dict[str, Any]) -> List[Dict[str, Any]]:
    if entry.get("type") != "mtp":
        return []
    return load_mtp_events_from_file(entry["file"])
