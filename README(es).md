# AsRecordedAPP

## Descripción

**AsRecordedAPP** es una aplicación de gestión de diálogos y toma de datos que facilita la organización y edición de información en hojas de Excel. Esta aplicación está construida utilizando PyQt5 para la interfaz gráfica de usuario y Pandas para la manipulación de datos en Excel.

## Tabla de Contenidos
- [Descripción](#descripción)
- [Características](#características)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Uso](#uso)
- [Contribuir](#contribuir)
- [Licencia](#licencia)
- [Contacto](#contacto)

## Características
- **Cargar y visualizar hojas de Excel**: Permite cargar cualquier archivo Excel y visualizar su contenido dentro de la aplicación.
- **Filtrar y buscar personajes y diálogos**: Búsqueda rápida a través de diálogos y personajes mediante un filtro avanzado.
- **Marcar intervenciones como completas**: Una opción para hacer seguimiento del progreso al marcar diálogos como completos.
- **Editar y guardar cambios en Excel**: Los cambios se guardan directamente en el archivo original, lo que facilita el flujo de trabajo.
- **Navegación entre tomas y personajes**: Navegación sencilla y rápida entre las diferentes tomas, con la posibilidad de filtrar por personaje.

## Estructura del Proyecto

```plaintext
AsRecordedAPP/
├── datahandler/
│   ├── __init__.py
│   ├── data_handler.py
│   ├── data_validator.py
│   ├── excel_handler.py
│   └── exceptions.py
├── gui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── main_widget.py
│   ├── gidoia_widget.py
│   ├── character_filter_dialog.py
│   ├── custom_widgets.py
│   └── utils.py
├── resources/
│   └── main.css
├── PreparacionExcel/
│   ├── Excel/
│   │   └── Excel de ejemplo
│   ├── scripts/
│   │   ├── CrearTxt.py  # Crea un txt adecuado para el programa con el word de referencia
│   │   └── PandasGuion.py  # Crea el xlsx usando el txt de referencia
│   ├── Txt/
│   │   └── Txt de ejemplo  # Recomendado como plantilla para trabajar con el programa
│   └── Word/
│       └── Word de ejemplo  # Específico del programa usado en la empresa
├── main.py
└── README.md
```

## Instalación

1. Ve a la carpeta que desees y clona este repositorio:

    ```sh
    git clone https://github.com/StablePeru/AsRecordedAPP.git
    cd AsRecordedAPP
    ```

2. Crea y activa un entorno virtual (opcional pero recomendado):

    ```sh
    python -m venv env
    ```

    2.1 En **Mac** y **Linux**:

    ```sh
    source env/bin/activate
    ```

    2.2 En **Windows**:

    ```sh
    env\Scripts\activate
    ```

3. Instala las dependencias:

    ```sh
    pip install -r requirements.txt
    ```

4. Si tienes problemas con la instalación de alguna dependencia, asegúrate de tener `pip` actualizado:

    ```sh
    python -m pip install --upgrade pip
    ```

## Uso

1. Ejecuta la aplicación:

    ```sh
    python main.py
    ```

2. Usa la interfaz para cargar y editar archivos de Excel, navegar entre tomas y personajes, y marcar intervenciones como completas.

## Contribuir

Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del proyecto.
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva característica'`).
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`).
5. Abre un Pull Request.

## Recursos
- [Documentación de PyQt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Documentación de Pandas](https://pandas.pydata.org/docs/)

## Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).

## Contacto

Para cualquier pregunta o sugerencia, por favor contacta a stableperu@gmail.com.
