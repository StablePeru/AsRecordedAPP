import pandas as pd

class DataHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.load_excel(file_path)
        
    def load_excel(self, file_path):
        try:
            self.xls = pd.ExcelFile(file_path)
            self.takes = self.xls.parse('Takes')
            self.intervenciones = self.xls.parse('Intervenciones')
        except FileNotFoundError:
            raise Exception(f"El archivo {file_path} no se encontró. Por favor, comprueba la ruta del archivo.")
        except Exception as e:
            raise Exception(f"Ocurrió un error al abrir el archivo {file_path}: {str(e)}")

    def get_take(self, take_number):
        if 'Numero Take' not in self.takes.columns:
            raise Exception("La columna 'Numero Take' no existe en self.takes.")
        return self.takes[self.takes['Numero Take'] == take_number]

    def get_dialogue(self, take_number):
        if 'Numero Take' not in self.intervenciones.columns:
            raise Exception("La columna 'Numero Take' no existe en la hoja 'Intervenciones'.")
        return self.intervenciones[self.intervenciones['Numero Take'] == take_number]

    def mark_complete(self, intervention_id, state):
        self.validate_columns(['ID', 'Completo'], self.intervenciones)
        self.intervenciones.loc[self.intervenciones['ID'] == intervention_id, 'Completo'] = state

    def update_dialogue(self, intervention_id, new_dialogue):
        self.validate_columns(['ID', 'Dialogo'], self.intervenciones)
        self.intervenciones.loc[self.intervenciones['ID'] == intervention_id, 'Dialogo'] = new_dialogue

    def save(self):
        try:
            with pd.ExcelWriter(self.file_path) as writer:
                self.takes.to_excel(writer, sheet_name='Takes', index=False)
                self.intervenciones.to_excel(writer, sheet_name='Intervenciones', index=False)
            print("Changes saved successfully.")
        except Exception as e:
            raise Exception(f"Ocurrió un error al guardar los cambios en el archivo de Excel: {str(e)}")
        
    def get_incomplete_characters(self):
        self.validate_columns(['Personaje', 'Completo'], self.intervenciones)
        incomplete_dialogues = self.intervenciones[self.intervenciones['Completo'] == 0]
        character_counts = incomplete_dialogues['Personaje'].value_counts().reset_index()
        character_counts.columns = ['Personaje', 'Takes Restantes']
        total_dialogues = self.intervenciones['Personaje'].value_counts().reset_index()
        total_dialogues.columns = ['Personaje', 'Total Takes']
        character_counts = pd.merge(character_counts, total_dialogues, on='Personaje')
        character_counts['Porcentaje Completado'] = 100 * (character_counts['Total Takes'] - character_counts['Takes Restantes']) / character_counts['Total Takes']
        return character_counts

    def get_next_incomplete_take(self, start_take):
        self.validate_columns(['Completo', 'Numero Take'], self.intervenciones)
        incomplete_takes = self.intervenciones[self.intervenciones['Completo'] == 0]['Numero Take'].unique()
        next_incomplete_take = incomplete_takes[incomplete_takes > start_take].min()
        return next_incomplete_take if pd.notna(next_incomplete_take) else None

    def get_character_names(self):
        self.validate_columns(['Personaje'], self.intervenciones)
        return self.intervenciones['Personaje'].unique().tolist()

    def update_timecode(self, intervention_id, timecode, save_after_update=True):
        self.validate_columns(['Hasiera'], self.intervenciones)
        self.intervenciones.loc[self.intervenciones['ID'] == intervention_id, 'Hasiera'] = timecode
        if save_after_update:
            self.save()

    def validate_columns(self, columns, df):
        missing_columns = [col for col in columns if col not in df.columns]
        if missing_columns:
            raise Exception(f"Las columnas siguientes no existen en el DataFrame: {', '.join(missing_columns)}")
