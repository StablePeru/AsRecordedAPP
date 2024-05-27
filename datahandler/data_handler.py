import pandas as pd
from .excel_handler import ExcelHandler
from .data_validator import DataValidator
from .exceptions import ColumnError

class DataHandler:
    def __init__(self, file_path):
        self.excel_handler = ExcelHandler(file_path)
        self.takes = self.excel_handler.takes
        self.intervenciones = self.excel_handler.intervenciones

    def get_take(self, take_number):
        DataValidator.validate_columns(['Numero Take'], self.takes)
        return self.takes[self.takes['Numero Take'] == take_number]

    def get_dialogue(self, take_number):
        DataValidator.validate_columns(['Numero Take'], self.intervenciones)
        return self.intervenciones[self.intervenciones['Numero Take'] == take_number]

    def mark_complete(self, intervention_id, state):
        DataValidator.validate_columns(['ID', 'Completo'], self.intervenciones)
        self.intervenciones.loc[self.intervenciones['ID'] == intervention_id, 'Completo'] = state

    def update_dialogue(self, intervention_id, new_dialogue):
        DataValidator.validate_columns(['ID', 'Dialogo'], self.intervenciones)
        self.intervenciones.loc[self.intervenciones['ID'] == intervention_id, 'Dialogo'] = new_dialogue

    def save(self):
        self.excel_handler.save()

    def get_incomplete_characters(self):
        DataValidator.validate_columns(['Personaje', 'Completo'], self.intervenciones)
        incomplete_dialogues = self.intervenciones[self.intervenciones['Completo'] == 0]
        character_counts = incomplete_dialogues['Personaje'].value_counts().reset_index()
        character_counts.columns = ['Personaje', 'Takes Restantes']
        total_dialogues = self.intervenciones['Personaje'].value_counts().reset_index()
        total_dialogues.columns = ['Personaje', 'Total Takes']
        character_counts = pd.merge(character_counts, total_dialogues, on='Personaje')
        character_counts['Porcentaje Completado'] = 100 * (character_counts['Total Takes'] - character_counts['Takes Restantes']) / character_counts['Total Takes']
        return character_counts

    def get_next_incomplete_take(self, start_take):
        DataValidator.validate_columns(['Completo', 'Numero Take'], self.intervenciones)
        incomplete_takes = self.intervenciones[self.intervenciones['Completo'] == 0]['Numero Take'].unique()
        next_incomplete_take = incomplete_takes[incomplete_takes > start_take].min()
        return next_incomplete_take if pd.notna(next_incomplete_take) else None

    def get_character_names(self):
        DataValidator.validate_columns(['Personaje'], self.intervenciones)
        return self.intervenciones['Personaje'].unique().tolist()

    def update_timecode(self, intervention_id, timecode, save_after_update=True):
        DataValidator.validate_columns(['Hasiera'], self.intervenciones)
        self.intervenciones.loc[self.intervenciones['ID'] == intervention_id, 'Hasiera'] = timecode
        if save_after_update:
            self.save()
