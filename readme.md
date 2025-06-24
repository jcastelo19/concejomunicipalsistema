# Sistema de Solicitudes Ciudadanas

Este proyecto es una aplicación de escritorio desarrollada en Python para la gestión y consulta de solicitudes ciudadanas. Permite registrar, consultar, editar y cambiar el estado de solicitudes, facilitando la atención y seguimiento de las mismas.

## Características

- Registro de nuevas solicitudes ciudadanas.
- Consulta y filtrado por cédula, tipo y rango de fechas.
- Edición y eliminación de solicitudes existentes.
- Cambio de estado de las solicitudes.
- Interfaz gráfica moderna usando [ttkbootstrap](https://ttkbootstrap.readthedocs.io/).

## Requisitos

- Python 3.10 o superior
- [ttkbootstrap](https://pypi.org/project/ttkbootstrap/)
- [tkcalendar](https://pypi.org/project/tkcalendar/)

## Instalación

1. Clona o descarga este repositorio.
2. Instala las dependencias ejecutando en la terminal:

   ```
   pip install -r requirements.txt
   ```

3. Asegúrate de que el archivo de base de datos `solicitudes.db` esté en la carpeta `database/`. Si no existe, puedes crearlo ejecutando el script de inicialización (si se provee) o la aplicación lo generará automáticamente.

## Uso

Ejecuta el archivo principal:

```
python main.py
```

La aplicación abrirá una ventana con pestañas para el dashboard, registro y consulta de solicitudes.

## Estructura del proyecto

```
Solicitud_ciudadana/
│
├── main.py
├── requirements.txt
├── README.md
├── database/
│   └── solicitudes.db
└── ui/
    ├── __init__.py
    ├── dashboard.py
    ├── registro.py
    └── consulta.py
```

## Notas

- Puedes modificar y ampliar la funcionalidad según las necesidades de tu comunidad.
- Si tienes problemas con dependencias o ejecución, revisa la versión de Python y los módulos instalados.

---

Desarrollado como parte de un proyecto de servicio comunitario.