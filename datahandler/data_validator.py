from .exceptions import ColumnError

class DataValidator:
    @staticmethod
    def validate_columns(columns, df):
        missing_columns = [col for col in columns if col not in df.columns]
        if missing_columns:
            raise ColumnError(f"Las columnas siguientes no existen en el DataFrame: {', '.join(missing_columns)}")
