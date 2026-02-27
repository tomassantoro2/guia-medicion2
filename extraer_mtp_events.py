"""
Extrae de la pestaña Events del MTP (Excel) los event_name y dataLayer
y guarda un JSON para integrar en generador_medicion.py
"""
import openpyxl
import json
import os

EXCEL_PATH = os.path.join(os.path.dirname(__file__), "MTP - Beautify PE - GA4 6jun2023 1.xlsx")
JSON_PATH = os.path.join(os.path.dirname(__file__), "mtp_events.json")


def extract_mtp_events():
    wb = openpyxl.load_workbook(EXCEL_PATH, read_only=True, data_only=True)
    if "Events" not in wb.sheetnames:
        raise ValueError("No se encontró la hoja 'Events' en el Excel")
    ws = wb["Events"]
    rows = list(ws.iter_rows(min_row=1, max_row=600, min_col=1, max_col=10, values_only=True))
    wb.close()

    # Filas donde empieza dataLayer.push (col E = index 4)
    starts = []
    for i, row in enumerate(rows):
        if row[4] and "dataLayer.push" in str(row[4]):
            starts.append(i)

    events_mtp = []
    for start_idx in starts:
        # Descripción "Event : ..." hacia atrás (col E)
        desc = ""
        for j in range(start_idx - 1, max(0, start_idx - 50), -1):
            if j < len(rows) and rows[j][4]:
                val = str(rows[j][4]).strip()
                if val.startswith("Event :") or (val.startswith("Event:") and len(val) > 10):
                    desc = val
                    break
                if "Script" in val and "Variable" in val:
                    break
        # Variable (col F=5), Values (col G=6) hasta });
        dl = {}
        for k in range(start_idx + 1, min(start_idx + 25, len(rows))):
            row = rows[k]
            script_line = row[4]
            if script_line and "});" in str(script_line):
                break
            var, val = row[5], row[6]
            if var and str(var).strip():
                key = str(var).strip()
                dl[key] = str(val).strip() if val is not None else ""
        event_name = dl.get("event_name", dl.get("event", ""))
        if not event_name and not dl:
            continue
        events_mtp.append({
            "event_name": event_name or desc[:50],
            "description": desc,
            "dl": dl,
        })

    return events_mtp


if __name__ == "__main__":
    events = extract_mtp_events()
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)
    print(f"Guardados {len(events)} eventos en {JSON_PATH}")
