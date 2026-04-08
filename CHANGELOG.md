# Changelog

Registro de ajustes relevantes al generador de guía de medición (`generador_medicion.py` y exportación Excel).

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
