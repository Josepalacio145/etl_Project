# loader.py
from sqlalchemy import create_engine
from etl.logger import get_logger
    
logger = get_logger(__name__)

def load_to_postgres(df, table_name, conn_string):
    try:
        engine = create_engine(conn_string)
        df.to_sql(table_name, engine, if_exists="append", index=False)
        logger.info(f"Cargado DataFrame a tabla {table_name} ({len(df)} filas)")
    except Exception as e:
        logger.error(f"Error al cargar datos en {table_name}: {e}", exc_info=True)