# Guía de medición (fase 2)

Aplicación **Streamlit** para documentar eventos de medición orientados a GA4: arma el `dataLayer.push`, capturas opcionales y exporta un Excel estilo Cerave para el equipo de desarrollo.

## Qué hace

- **Inicio** (`generador_medicion.py`): flujo en **pasos numerados** (Context → Event setup → Configure payload → Review & add). Elegís **Custom**, **plantilla GA4 recomendada** o un **catálogo MTP** desde `catalogs/manifest.json`. El nombre GA4 para documentación (columna Excel) va en **Event setup** como primer campo; luego fuente del evento, tipo de elemento, disparo y captura; catálogo MTP con tabla seleccionable, paginación y detalle. Tras **Add event to guide**, la sesión se limpia para el siguiente evento y el foco vuelve al inicio del paso 2 (mismo comportamiento para MTP, GA4 y Custom).
- **Guía y exportación** (`pages/2_Guide_Export.py`, enlace en la Home): cola de eventos, diccionario opcional Key/Value, descarga Excel; también en pasos con tarjetas (`border`).
- **Interfaz**: tema editorial **mid** (fondo cálido, textura ligera) en `.streamlit/config.toml` y CSS en `measurement_guide/ui_theme.py`; interruptor **Dark theme** (menos brillo). Barra lateral **colapsada** al cargar (`initial_sidebar_state="collapsed"`).
- **Excel**: primera hoja **Guide overview** (fecha UTC, versión de export, tabla resumen por evento con Page/URL, entorno, notas, GA4, tipo de elemento; bloque opcional Key/Value); hoja **Measurement Guide** con el layout Cerave de cinco columnas (Screenshot, how, Script, Variable/Values).
- **Catálogos**: `catalogs/mtp_events.json` (extracción MTP), `catalogs/ga4_recommended.json` (plantillas). El manifiesto `catalogs/manifest.json` registra qué JSON MTP se ofrece en la UI.

## Archivos principales

| Ruta | Rol |
|------|-----|
| `generador_medicion.py` | Entrada Streamlit (Home) |
| `pages/2_Guide_Export.py` | Cola y descarga Excel |
| `measurement_guide/` | Builders de script, export Excel, modelos, carga de catálogos, `ui_theme.py` (tema y foco post–add event) |
| `.streamlit/config.toml` | Colores base Streamlit y `toolbarMode` (ver también tema en `ui_theme.py`) |
| `catalogs/` | `manifest.json`, JSON MTP, plantillas GA4 |
| `DOCUMENTATION.md` | Contrato de exportación (dataLayer vs nombre GA4) |
| `extraer_mtp_events.py` | CLI para regenerar el JSON MTP desde Excel |

## Extractor MTP (Excel → JSON)

Layout esperado (mismo criterio que la plantilla Beautify PE): hoja **Events**; fragmentos en columna **E**; nombres de variable en **F**; valores en **G** (filas posteriores a cada `dataLayer.push`).

```text
python extraer_mtp_events.py --excel "ruta/al/MTP.xlsx" --sheet Events -o catalogs/mtp_events.json
```

Por defecto, salida en `catalogs/mtp_events.json` si el Excel por defecto existe en el proyecto.

## Requisitos y ejecución local

- Python 3.10+ recomendado.
- Dependencias: `pip install -r requirements.txt` (incluye **Streamlit ≥ 1.35** por selección de filas en `st.dataframe`).

```text
streamlit run generador_medicion.py
```

Abre la URL que muestre la consola (por defecto `http://localhost:8501`).
