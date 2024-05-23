import pandas as pd
import re
from tkinter import filedialog
from tkinter import Tk

# Función para seleccionar archivo de guion
def seleccionar_archivo():
    root = Tk()
    root.withdraw()  # Ocultar la ventana de Tkinter
    archivo = filedialog.askopenfilename()  # Ventana para seleccionar archivo
    return archivo

# Función para seleccionar directorio para guardar archivo de Excel
def seleccionar_directorio():
    root = Tk()
    root.withdraw()
    directorio = filedialog.asksaveasfilename(defaultextension='.xlsx')  # Ventana para guardar archivo
    return directorio

# Función para procesar guion
def procesar_guion(archivo):
    with open(archivo, 'r') as file:
        contenido = file.readlines()

    # Datos para Takes e Intervenciones
    datos_takes = {'Numero Take': [], 'IN': [], 'OUT': []}
    datos_intervenciones = {'ID': [], 'Numero Take': [], 'Personaje': [], 'Dialogo': [], 'Completo': []}

    # Variables para guardar el take y personaje actual
    take_actual = None
    personaje_actual = None
    dialogo_actual = ""
    id_counter = 0  # Contador para el ID

    def guardar_intervencion():
        """Función auxiliar para guardar una intervención."""
        nonlocal id_counter, personaje_actual, dialogo_actual
        if personaje_actual is not None:  # Si había un personaje y diálogo anteriores, añadirlos a los datos
            datos_intervenciones['ID'].append(id_counter)
            datos_intervenciones['Numero Take'].append(take_actual)
            datos_intervenciones['Personaje'].append(personaje_actual)
            datos_intervenciones['Dialogo'].append(dialogo_actual.strip())
            datos_intervenciones['Completo'].append(0)  # Completo siempre es 0
            id_counter += 1  # Incrementar el contador de ID
            personaje_actual = None
            dialogo_actual = ""

    # Recorrer el contenido línea por línea
    for linea in contenido:
        if linea.startswith("TAKE:"):
            guardar_intervencion()  # Guardar intervención antes de pasar al siguiente take
            take_actual = re.findall(r'TAKE: (\d+)', linea)[0]
            datos_takes['Numero Take'].append(take_actual)
        elif linea.startswith("IN:"):
            in_time = re.findall(r'IN: (\d+:\d+:\d+:\d+)', linea)[0]
            datos_takes['IN'].append(in_time)
        elif linea.startswith("OUT:"):
            out_time = re.findall(r'OUT: (\d+:\d+:\d+:\d+)', linea)[0]
            datos_takes['OUT'].append(out_time)
        else:  # Esto debe ser una intervención
            intervencion = re.findall(r'([A-Z\s\d]+:)\s*(.*?)$', linea)
            if intervencion:  # Si se encuentra un nuevo personaje y/o diálogo
                guardar_intervencion()  # Guardar la intervención anterior antes de actualizar el personaje y diálogo
                personaje_actual = intervencion[0][0].strip(":")
                dialogo_actual = intervencion[0][1]
            else:  # Si no se encuentra un nuevo personaje, asumir que es una continuación del diálogo actual
                dialogo_actual += " " + linea.strip()

    guardar_intervencion()  # Asegurarse de añadir la última intervención

    return datos_takes, datos_intervenciones


# Función para crear archivo de Excel
def crear_excel(datos_takes, datos_intervenciones, directorio):
    # Crear dataframes
    df_takes = pd.DataFrame(datos_takes)
    df_intervenciones = pd.DataFrame(datos_intervenciones)

    # Crear archivo de Excel con dos hojas
    with pd.ExcelWriter(directorio) as writer:
        df_takes.to_excel(writer, sheet_name='Takes', index=False)
        df_intervenciones.to_excel(writer, sheet_name='Intervenciones', index=False)

# Función principal
def main():
    # Seleccionar archivo de guion
    archivo = seleccionar_archivo()
    
    # Procesar guion
    datos_takes, datos_intervenciones = procesar_guion(archivo)
    
    # Seleccionar directorio para guardar archivo de Excel
    directorio = seleccionar_directorio()
    
    # Crear archivo de Excel
    crear_excel(datos_takes, datos_intervenciones, directorio)

if __name__ == "__main__":
    main()
