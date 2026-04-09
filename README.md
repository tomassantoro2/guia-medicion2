# Guía de medición (fase 2)

Aplicación **Streamlit** para documentar eventos de medición orientados a GA4: arma el `dataLayer.push`, capturas opcionales y exporta un Excel estilo Cerave para el equipo de desarrollo.

## Qué hace

- **Inicio** (`generador_medicion.py`): elegís **Custom**, **plantilla GA4 recomendada** o un **catálogo MTP** definido en `catalogs/manifest.json`; completás URL de página, entorno, notas y nombre GA4 (columna de documentación); previsualizás y agregás eventos a la cola.
- **Guía y exportación** (barra lateral, `pages/2_Guide_Export.py`): revisás la cola, duplicás o quitás filas y descargás el Excel.
- **Excel**: primera hoja **Guide overview** (fecha UTC, versión de export, tabla resumen por evento con Page/URL, entorno, notas, GA4, tipo de elemento; bloque opcional Key/Value); hoja **Measurement Guide** con el layout Cerave de cinco columnas (Screenshot, how, Script, Variable/Values).
- **Catálogos**: `catalogs/mtp_events.json` (extracción MTP), `catalogs/ga4_recommended.json` (plantillas). El manifiesto `catalogs/manifest.json` registra qué JSON MTP se ofrece en la UI.

## Archivos principales

| Ruta | Rol |
|------|-----|
| `generador_medicion.py` | Entrada Streamlit (Home) |
| `pages/2_Guide_Export.py` | Cola y descarga Excel |
| `measurement_guide/` | Builders de script, export Excel, modelos, carga de catálogos |
| `catalogs/` | `manifest.json`, JSON MTP, plantillas GA4 |
| `DOCUMENTATION.md` | Contrato de exportación (dataLayer vs nombre GA4) |
| `extraer_mtp_events.py` | CLI para regenerar el JSON MTP desde Excel |

## Extractor MTP (Excel → JSON)

Layout esperado (mismo criterio que la plantilla Beautify PE): hoja **Events**; fragmentos en columna **E**; nombres de variable en **F**; valores en **G** (filas posteriores a cada `dataLayer.push`).

```text
python extraer_mtp_events.py --excel "ruta/al/MTP.xlsx" --sheet Events -o catalogs/mtp_events.json
```

Por defecto, salida en `catalogs/mtp_events.json` si el Excel por defecto existe en el proyecto.
