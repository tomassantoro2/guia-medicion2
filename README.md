# Guía de medición (Fase 1)

Herramienta web con **Streamlit** para documentar eventos de medición: armás el `dataLayer.push`, agregás capturas y exportás un Excel con formato tipo guía Cerave (columnas Screenshot, how it is triggered, Script, Variable, Values).

## Requisitos

- **Python 3.10+** (recomendado 3.12)
- Dependencias listadas en `requirements.txt`

## Instalación

```bash
cd guia-medicion2
python -m pip install -r requirements.txt
```

En Windows, si el comando `python` abre la Microsoft Store, usá la ruta del instalador oficial, por ejemplo:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -m pip install -r requirements.txt
```

## Ejecución

```bash
python -m streamlit run generador_medicion.py
```

Se abre en el navegador, por defecto en `http://localhost:8501`.

## Archivos principales

| Archivo | Descripción |
|--------|-------------|
| `generador_medicion.py` | App Streamlit: formulario, preview JS, lista de eventos y descarga Excel. |
| `mtp_events.json` | Eventos importados del MTP (Beautify PE); si existe, podés elegir “Evento del MTP” en la UI. |
| `extraer_mtp_events.py` | Script para regenerar `mtp_events.json` desde un Excel del MTP (hoja `Events`). Requiere el archivo `.xlsx` local con el nombre configurado en el script. |

## Eventos MTP (opcional)

Si tenés el Excel del MTP en la carpeta del proyecto (nombre esperado en `extraer_mtp_events.py`), podés ejecutar:

```bash
python extraer_mtp_events.py
```

Eso vuelve a generar `mtp_events.json`.

## Trabajar con Git y GitHub

Este clon ya tiene configurado el remoto `origin` apuntando al repositorio en GitHub:

- **Repositorio:** `https://github.com/tomassantoro2/guia-medicion2`

### Traer cambios del remoto

```bash
git pull origin main
```

### Subir tus cambios

```bash
git add .
git status
git commit -m "Descripción breve del cambio"
git push origin main
```

La primera vez que hagas `git push` desde esta máquina, Git te pedirá autenticación. Opciones habituales:

- **HTTPS:** un *Personal Access Token* de GitHub en lugar de la contraseña de la cuenta.
- **SSH:** clave SSH configurada en GitHub y remoto `git@github.com:usuario/guia-medicion2.git`.

Si usás **tu propio fork** u otro repo, cambiá la URL del remoto:

```bash
git remote set-url origin https://github.com/TU_USUARIO/guia-medicion2.git
```

Comprobá la configuración con:

```bash
git remote -v
```

## Licencia

Definir según el acuerdo del equipo / del repositorio original.
