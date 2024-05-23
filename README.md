# As Recorded

Este proyecto tiene como objetivo crear guiones "As Recorded" para el mundo del doblaje. 

## Estructura del Proyecto

### PreparacionExcel

Esta carpeta contiene tres subcarpetas y dos scripts para transformar los guiones:

- **Word/**: Carpeta para los archivos de guiones en formato DOCX.
- **Txt/**: Carpeta para los archivos de guiones en formato TXT.
- **Excel/**: Carpeta para los archivos de guiones en formato XLSX.
- **scripts/**
  - `CrearTxt.py`: Convierte los guiones en formato DOCX a TXT.
  - `PandasGuion.py`: Convierte los archivos TXT en archivos Excel listos para trabajar en la aplicación.

### Main

Esta carpeta contiene los archivos principales para la interfaz gráfica de usuario y el manejo de datos:

- `main.css`: Contiene el estilo de la interfaz de usuario.
- `gui.py`: Contiene el código para manejar la interfaz gráfica de usuario utilizando PyQt5.
- `datahandler.py`: Encargado de manejar los datos de Excel utilizando pandas.

## Uso

### 1. Clona este repositorio:

```
git clone https://github.com/StablePeru/AsRecorded.git
cd AsRecorded
```

### 2. Instala las dependencias:
```
pip install -r requirements.txt
```

### 3. Ejecuta la aplicación GUI:
```
python Main/gui.py
```

## Descripción de los Scripts

### CrearTxt.py
Este script convierte los guiones originales en formato DOCX a un formato TXT, facilitando su manipulación.

#### Funciones Principales:
- **select_file()**: Selecciona el archivo DOCX.
- **select_folder()**: Selecciona la carpeta de destino para el archivo TXT.
- **read_word_file(file_path)**: Lee el archivo DOCX y extrae el texto.
- **save_to_txt(text, folder_path)**: Guarda el texto extraído en un archivo TXT.

### PandasGuion.py
Este script convierte los archivos TXT en archivos Excel (XLSX) con el formato necesario para trabajar en la aplicación.

#### Funciones Principales:
- **seleccionar_archivo()**: Selecciona el archivo TXT.
- **seleccionar_directorio()**: Selecciona el directorio de destino para el archivo Excel.
- **procesar_guion(archivo)**: Procesa el archivo TXT y extrae los datos.
- **crear_excel(datos_takes, datos_intervenciones, directorio)**: Crea el archivo Excel con dos hojas (Takes e Intervenciones).

### datahandler.py
Este script maneja los datos de los archivos Excel, utilizando la biblioteca pandas.

#### Clases y Métodos Principales:
- **DataHandler**: Clase principal para manejar los datos de Excel.
- **load_excel(file_path)**: Carga el archivo Excel.
- **get_take(take_number)**: Obtiene la información de un take específico.
- **get_dialogue(take_number)**: Obtiene los diálogos de un take específico.
- **mark_complete(intervention_id, state)**: Marca una intervención como completa.
- **update_dialogue(intervention_id, new_dialogue)**: Actualiza el diálogo de una intervención.
- **save()**: Guarda los cambios en el archivo Excel.
- **get_incomplete_characters()**: Obtiene los personajes con diálogos incompletos.
- **get_next_incomplete_take(start_take)**: Obtiene el siguiente take incompleto.
- **get_character_names()**: Obtiene los nombres de los personajes.
- **update_timecode(intervention_id, timecode, save_after_update=True)**: Actualiza el código de tiempo de una intervención.

### gui.py
Este script contiene el código para manejar la interfaz gráfica de usuario utilizando PyQt5.

#### Componentes Principales:
- **CharacterLabel**: Clase para los labels de personajes.
- **CustomMessageBox**: Clase para personalizar los MessageBox.
- **MainWidget**: Widget principal de la aplicación.
- **TimecodeLineEdit**: Campo de edición para los códigos de tiempo.
- **GidoiaWidget**: Widget para manejar los diálogos y takes.
- **Application**: Clase principal de la aplicación.

### main.css
Este archivo contiene el estilo de la interfaz de usuario para asegurar una apariencia consistente y agradable.

#### Estilos Principales:
- **QWidget**: Estilo general para los widgets.
- **QPushButton**: Estilo para los botones.
- **QLabel**: Estilo para los labels.
- **QLineEdit y QPlainTextEdit**: Estilo para los campos de texto.
- **QTableWidget**: Estilo para las tablas.

### Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request si deseas colaborar.
