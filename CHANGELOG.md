# Changelog

Registro de ajustes relevantes al generador de guía de medición (`generador_medicion.py` y exportación Excel).

## 2026-04-09

### Interfaz (Streamlit)

- **Pasos numerados** en la Home (1–4) y en **Guide & export** (1–2), con bloques `st.container(border=True)` y estilos en `measurement_guide/ui_theme.py` (tema editorial **mid**: fondo cálido, textura SVG, acentos terracota; opción **Dark theme** vía interruptor en sesión).
- **`.streamlit/config.toml`**: colores alineados al tema mid, `toolbarMode = minimal`, `initial_sidebar_state="collapsed"` en Home y página de exportación.
- **Event setup**: el campo **GA4 event name (documentation column)** es el primero del paso 2; **Context** queda solo con URL, entorno y notas.
- **MTP**: tabla con `st.dataframe` (`selection_mode="single-row"`, `on_select="rerun"`); paginación bajo la tabla; limpieza ampliada de claves de sesión al añadir un evento (incl. `mtp_*` / `mtp_catalog`).
- Tras **Add event to guide**, comportamiento **único** para MTP, GA4 y Custom: reinicio de campos del evento y script de foco/scroll al primer campo del paso 2 (`render_new_event_start_focus_if_needed`).
- **`requirements.txt`**: `streamlit>=1.35.0`.

### Documentación

- **README**: descripción actualizada del flujo, tema, ejecución local y tabla de archivos.

## 2026-04-08

### Interfaz (Streamlit)

- Textos de la interfaz pasados de español a **inglés**, manteniendo un tono formal.
- Eliminados los **checkboxes** de `eventCategory`, `eventAction` y `eventLabel`. Cada campo es opcional: si queda vacío (o solo espacios), **no se incluye** en el `dataLayer` resultante.
- Vista previa de `dataLayer.push` alineada con el formato legible (multilínea) usado en la exportación.

### Exportación Excel

- **Encabezados** con estilo (fondo azul oscuro, texto blanco, bordes).
- **Celdas combinadas** en columnas A–C (Screenshot, how it is triggered, Script) para igualar la altura del bloque de **Variable / Values**.
- Columna **Script** con fuente monoespaciada (**Consolas**) y `dataLayer.push` en formato **JavaScript multilínea** (saltos de línea y sangría), incluyendo etiquetas `<script>`.
- **Screenshot**: columna A dimensionada para la imagen; altura de filas con **mínimo** para evitar filas ilegibles al repartir altura entre muchas filas.
- **Columnas D y E**: reducido el espacio vacío previo a la primera variable (una fila de separación en lugar de dos); **una fila en blanco** entre eventos consecutivos por estética.
- Bordes y alineación en celdas del cuerpo; hoja titulada *Measurement Guide*.

### Otros

- Eliminado import no usado (`csv`).
- Ajustes previos de documentación en **README** (descripción funcional de la herramienta, sin instrucciones de instalación/Git).
