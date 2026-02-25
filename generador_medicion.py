import streamlit as st
import csv
import io
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.drawing.image import Image as XLImage

st.set_page_config(page_title="Guía de Medición – Fase 1", layout="centered")

if "events" not in st.session_state:
    st.session_state.events = []

if "extra_params" not in st.session_state:
    st.session_state.extra_params = []

st.title("📏 Generador de Guía de Medición")
st.caption("Fase 1 · Eventos custom · dataLayer.push")

event_type = st.selectbox(
    "Tipo de evento",
    ["Botón", "Banner", "Link"],
    key="event_type"
)

how_triggered = st.text_area(
    "How it is triggered",
    placeholder="Ej: Cuando el usuario hace click en el botón HotSale del home",
    key="how_triggered"
)

screenshot_file = st.file_uploader(
    "📷 Captura de pantalla (Screenshot)",
    type=["png", "jpg", "jpeg"],
    key="screenshot_upload",
    help="Subí una imagen para que aparezca en la columna Screenshot del Excel"
)
if screenshot_file is not None:
    st.image(screenshot_file, caption="Vista previa", use_container_width=False, width=200)

event_base = st.selectbox(
    "Evento GTM (event)",
    ["uaevent", "nievent", "socialInt", "Custom"],
    key="event_base"
)

# 👇 Cuando elegís Custom, aparece el campo para poner el nombre que quieras
if event_base == "Custom":
    event_value = st.text_input(
        "Nombre del event custom",
        placeholder="Ej: mi_evento_personalizado",
        key="event_custom"
    )
else:
    event_value = event_base

event_name = st.text_input(
    "event_name (sugerido)",
    placeholder="Ej: apretar_boton",
    key="event_name"
)

st.markdown("### Parámetros sugeridos")

use_category = st.checkbox("eventCategory", value=True, key="use_category")
eventCategory = st.text_input(
    "Valor eventCategory",
    value="interaction",
    key="eventCategory"
)

use_action = st.checkbox("eventAction", value=True, key="use_action")
eventAction = st.text_input(
    "Valor eventAction",
    value="click",
    key="eventAction"
)

use_label = st.checkbox("eventLabel", value=False, key="use_label")
eventLabel = st.text_input(
    "Valor eventLabel",
    value=event_name or "",
    key="eventLabel"
)

st.markdown("### Parámetros adicionales")
st.caption("Agregá todos los que necesites. Escribí nombre y valor, luego click en Agregar.")

col_extra1, col_extra2, col_extra3 = st.columns([2, 2, 1])
with col_extra1:
    extra_key = st.text_input("Nombre", key="extra_key", label_visibility="collapsed", placeholder="Nombre del parámetro")
with col_extra2:
    extra_value = st.text_input("Valor", key="extra_value", label_visibility="collapsed", placeholder="Valor del parámetro")
with col_extra3:
    st.write("")  # Espacio para alinear
    if st.button("➕ Agregar", key="add_extra_param"):
        if extra_key and extra_value:
            st.session_state.extra_params.append({"key": extra_key, "value": extra_value})
            if "extra_key" in st.session_state:
                del st.session_state["extra_key"]
            if "extra_value" in st.session_state:
                del st.session_state["extra_value"]
            st.rerun()

# Mostrar parámetros agregados
if st.session_state.extra_params:
    st.caption("Parámetros agregados:")
    for i, p in enumerate(st.session_state.extra_params):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.text(p["key"])
        with col2:
            st.text(p["value"])
        with col3:
            if st.button("🗑️", key=f"del_param_{i}"):
                st.session_state.extra_params.pop(i)
                st.rerun()

# -------------------------
# Build dataLayer preview (incluye TODOS los parámetros adicionales)
# -------------------------
dl = {}

if event_value:
    dl["event"] = str(event_value)

if event_name:
    dl["event_name"] = str(event_name)

if use_category:
    dl["eventCategory"] = str(eventCategory)

if use_action:
    dl["eventAction"] = str(eventAction)

if use_label:
    dl["eventLabel"] = str(eventLabel)

# Agregar todos los parámetros adicionales (no solo uno)
for p in list(st.session_state.extra_params):
    dl[str(p["key"])] = str(p["value"])

st.markdown("### 📜 Preview dataLayer.push")

# Escapar comillas en los valores para el código JavaScript
def safe_js_value(v):
    return str(v).replace('\\', '\\\\').replace('"', '\\"')

st.code(
    "dataLayer.push({\n" +
    ",\n".join([f'  {k}: "{safe_js_value(v)}"' for k, v in dl.items()]) +
    "\n});",
    language="javascript"
)

# Solo se envía al hacer click en el botón (Enter ya no envía)
if st.button("➕ Agregar evento a la guía", type="primary"):
    if not event_value:
        st.error("Tenés que definir el event (uaevent / custom / etc).")
    elif not event_name:
        st.error("Tenés que definir un event_name.")
    elif event_base == "Custom" and not st.session_state.get("event_custom"):
        st.error("Si elegís Custom, tenés que completar el nombre del event.")
    else:
        screenshot_bytes = screenshot_file.read() if screenshot_file else None
        st.session_state.events.append({
            "type": event_type,
            "how": how_triggered,
            "datalayer": dl,
            "screenshot": screenshot_bytes
        })
        st.success("Evento agregado a la guía")

        # Borrar todos los campos excepto parámetros adicionales (esos se borran a mano)
        keys_to_clear = [
            "event_type", "how_triggered", "event_base", "event_custom",
            "event_name", "use_category", "eventCategory",
            "use_action", "eventAction", "use_label", "eventLabel",
            "extra_key", "extra_value", "screenshot_upload"
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

st.divider()
st.subheader("📄 Eventos en la guía")

if not st.session_state.events:
    st.info("Todavía no agregaste eventos")
else:
    # Formato estilo Guía Cerave para Excel: Screenshot | how it is triggered | Script | Variable | Values
    headers = ["Screenshot", "how it is triggered", "Script", "Variable", "Values"]

    def build_script(dl):
        """Genera el script dataLayer.push con comillas simples (formato entregable)"""
        def escape_single(s):
            return str(s).replace("\\", "\\\\").replace("'", "\\'")
        parts = [f"'{escape_single(k)}': '{escape_single(v)}'" for k, v in dl.items()]
        return f"<script>dataLayer.push({{{', '.join(parts)}}});</script>"

    wb = Workbook()
    ws = wb.active
    ws.title = "Guía de Medición"

    # Header con estilo
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(wrap_text=True, vertical="top")

    row_num = 2
    for ev in st.session_state.events:
        how = ev["how"] or ""
        script = build_script(ev["datalayer"])
        screenshot_bytes = ev.get("screenshot")

        # Fila 1: screenshot + how triggered + script completo
        ws.cell(row=row_num, column=1, value="")
        ws.cell(row=row_num, column=2, value=how)
        ws.cell(row=row_num, column=3, value=script)
        ws.cell(row=row_num, column=4, value="")
        ws.cell(row=row_num, column=5, value="")
        ws.cell(row=row_num, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=row_num, column=3).alignment = Alignment(wrap_text=True, vertical="top")

        # Insertar imagen en columna Screenshot si existe
        if screenshot_bytes:
            try:
                img = XLImage(io.BytesIO(screenshot_bytes))
                # Redimensionar si es muy grande (Excel se ve bien con ~200px de ancho)
                max_width = 180
                if img.width > max_width:
                    ratio = max_width / img.width
                    img.width = int(img.width * ratio)
                    img.height = int(img.height * ratio)
                cell_ref = f"A{row_num}"
                ws.add_image(img, cell_ref)
                # Ajustar altura de fila para que se vea la imagen (~0.75 pt por pixel)
                ws.row_dimensions[row_num].height = max(60, min(400, img.height * 0.75))
            except Exception:
                ws.cell(row=row_num, column=1, value="[Imagen no válida]")

        row_num += 1

        # Fila vacía
        row_num += 1

        # Filas Variable | Values
        for var, val in ev["datalayer"].items():
            ws.cell(row=row_num, column=4, value=var)
            ws.cell(row=row_num, column=5, value=str(val))
            row_num += 1

        # Fila vacía entre eventos
        row_num += 1

    # Ajustar ancho de columnas
    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 45
    ws.column_dimensions["C"].width = 80
    ws.column_dimensions["D"].width = 20
    ws.column_dimensions["E"].width = 35

    # Guardar en memoria
    excel_buffer = io.BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)

    # Botón de descarga
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"guia_medicion_{ts}.xlsx"

    st.download_button(
        label="📥 Descargar Excel (formato Guía Cerave)",
        data=excel_buffer,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_excel"
    )

    st.write("")  # Espacio

    for i, ev in enumerate(st.session_state.events, start=1):
        with st.expander(f"Evento {i}"):
            if ev.get("screenshot"):
                st.image(io.BytesIO(ev["screenshot"]), caption="Screenshot", width=200)
            st.write("**Cómo se dispara:**")
            st.write(ev["how"])
            st.write("**dataLayer:**")
            st.json(ev["datalayer"])
