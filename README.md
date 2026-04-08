# Guía de medición (Fase 1)

Interfaz web (**Streamlit**) para armar la documentación de eventos de medición basados en `dataLayer.push` y en el modelo de eventos del MTP (Beautify PE).

## Qué hace

- Permite definir **eventos personalizados**: tipo de elemento (botón, banner, link), texto de *how it is triggered*, captura de pantalla opcional, y parámetros del dataLayer (evento GTM, `event_name`, `eventCategory` / `eventAction` / `eventLabel` y pares nombre–valor adicionales).
- Si en el proyecto existe **`mtp_events.json`**, también podés elegir **eventos precargados del MTP**: el dataLayer se completa según el evento seleccionado (descripción y variables definidas en ese catálogo).
- Muestra en pantalla un **preview en JavaScript** del `dataLayer.push` correspondiente.
- Acumula los eventos en una **guía** y genera un **Excel** con formato tipo guía Cerave: columnas **Screenshot**, **how it is triggered**, **Script** (el snippet con `dataLayer.push`), y desglose por **Variable** y **Values** para cada clave del objeto enviado al dataLayer.

## Archivos que forman parte de la herramienta

| Archivo | Rol |
|--------|-----|
| `generador_medicion.py` | Aplicación: formularios, preview, lista de eventos y exportación del Excel. |
| `mtp_events.json` | Catálogo de eventos MTP (nombre, descripción y objeto `dl`) usado cuando elegís origen MTP en la interfaz. |
| `extraer_mtp_events.py` | Utilidad orientada al mismo flujo de datos: a partir del Excel del MTP (hoja `Events`) permite volver a generar `mtp_events.json` cuando actualizás el documento fuente. |
