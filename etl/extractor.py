# extractor.py
import pandas as pd
from pathlib import Path
from etl.logger import get_logger 


logger = get_logger(__name__)

def read_excels(input_dir: str) -> dict:
    logger.info(f"Leyendo archivos desde {input_dir}")
    #excel_files = Path(input_dir).glob("*.xlsx")
    excel_files = list(Path(input_dir).glob("*.xlsx"))
    
    if not excel_files:
        logger.warning("No se encontraron archivos Excel en la ruta")
        
    dataframes = {}
    for file in excel_files:
        try:
            df = pd.read_excel(file)
            #dataframes[file.stem] = df
            dataframes[file.stem] = {"df": df, "path": file}
            logger.info(f"Archivo {file.name} leído correctamente con {len(df)} filas")
        except Exception as e:
            logger.error(f"Error leyendo {file.name}: {e}", exc_info=True)

    return dataframes
