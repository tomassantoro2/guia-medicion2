import streamlit as st
import csv
import io
from datetime import datetime

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
        st.session_state.events.append({
            "type": event_type,
            "how": how_triggered,
            "datalayer": dl
        })
        st.success("Evento agregado a la guía")

        # Borrar todos los campos excepto parámetros adicionales (esos se borran a mano)
        keys_to_clear = [
            "event_type", "how_triggered", "event_base", "event_custom",
            "event_name", "use_category", "eventCategory",
            "use_action", "eventAction", "use_label", "eventLabel",
            "extra_key", "extra_value"
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
    # Formato estilo Guía Cerave: Screenshot | how it is triggered | Script | Variable | Values
    headers = ["Screenshot", "how it is triggered", "Script", "Variable", "Values"]

    def build_script(dl):
        """Genera el script dataLayer.push con comillas simples (formato entregable)"""
        def escape_single(s):
            return str(s).replace("\\", "\\\\").replace("'", "\\'")
        parts = [f"'{escape_single(k)}': '{escape_single(v)}'" for k, v in dl.items()]
        return f"<script>dataLayer.push({{{', '.join(parts)}}});</script>"

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)

    for ev in st.session_state.events:
        how = ev["how"] or ""
        script = build_script(ev["datalayer"])

        # Fila 1: how triggered + script completo
        writer.writerow(["", how, script, "", ""])
        # Fila vacía
        writer.writerow(["", "", "", "", ""])
        # Filas Variable | Values (una por cada parámetro del datalayer)
        for var, val in ev["datalayer"].items():
            writer.writerow(["", "", "", var, str(val)])
        # Fila vacía entre eventos
        writer.writerow(["", "", "", "", ""])

    csv_content = output.getvalue()

    # Botón de descarga
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"guia_medicion_{ts}.csv"

    st.download_button(
        label="📥 Descargar CSV (formato Guía Cerave)",
        data=csv_content.encode("utf-8-sig"),
        file_name=filename,
        mime="text/csv",
        key="download_csv"
    )

    st.write("")  # Espacio

    for i, ev in enumerate(st.session_state.events, start=1):
        with st.expander(f"Evento {i}"):
            st.write("**Cómo se dispara:**")
            st.write(ev["how"])
            st.write("**dataLayer:**")
            st.json(ev["datalayer"])
