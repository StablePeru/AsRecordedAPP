import pandas as pd
from .exceptions import FileNotFoundError, ColumnError

class ExcelHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.load_excel(file_path)

    def load_excel(self, file_path):
        try:
            self.xls = pd.ExcelFile(file_path)
            self.takes = self.xls.parse('Takes')
            self.intervenciones = self.xls.parse('Intervenciones')
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo {file_path} no se encontró. Por favor, comprueba la ruta del archivo.")
        except Exception as e:
            raise Exception(f"Ocurrió un error al abrir el archivo {file_path}: {str(e)}")

    def save(self):
        try:
            with pd.ExcelWriter(self.file_path) as writer:
                self.takes.to_excel(writer, sheet_name='Takes', index=False)
                self.intervenciones.to_excel(writer, sheet_name='Intervenciones', index=False)
            print("Changes saved successfully.")
        except Exception as e:
            raise Exception(f"Ocurrió un error al guardar los cambios en el archivo de Excel: {str(e)}")
