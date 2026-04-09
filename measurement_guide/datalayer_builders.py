"""dataLayer.push formatting for Excel export and Streamlit preview."""


def _escape_js_single(s: str) -> str:
    return str(s).replace("\\", "\\\\").replace("'", "\\'")


def build_measurement_script_excel(dl: dict) -> str:
    """Multi-line <script> + dataLayer.push for Excel (single-quoted, readable layout)."""
    if not dl:
        return "<script>\ndataLayer.push({});\n</script>"
    lines = ["<script>", "dataLayer.push({"]
    items = list(dl.items())
    for i, (k, v) in enumerate(items):
        comma = "," if i < len(items) - 1 else ""
        lines.append(f"  '{_escape_js_single(k)}': '{_escape_js_single(v)}'{comma}")
    lines.append("});")
    lines.append("</script>")
    return "\n".join(lines)


def _safe_js_double_quoted(v) -> str:
    return str(v).replace("\\", "\\\\").replace('"', '\\"')


def build_measurement_script_preview(dl: dict) -> str:
    """Pretty dataLayer.push for Streamlit preview (double-quoted, no script tags)."""
    if not dl:
        return "dataLayer.push({});"
    lines = ["dataLayer.push({"]
    items = list(dl.items())
    for i, (k, v) in enumerate(items):
        comma = "," if i < len(items) - 1 else ""
        lines.append(f'  {k}: "{_safe_js_double_quoted(v)}"{comma}')
    lines.append("});")
    return "\n".join(lines)
