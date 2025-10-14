from sqlalchemy import create_engine, text
from etl.logger import get_logger


logger = get_logger(__name__)

def call_stored_procedure(db_connection: str, procedure_name: str):
    """
    Llama a un stored procedure en PostgreSQL.
    """
    engine = create_engine(db_connection)
    with engine.connect() as conn:
        conn.execute(text(f"call {procedure_name}();"))    
        logger.info(f"Abre conexión: {engine} )")

        def call_stored_procedure(db_connection: str, procedure_name: str):
            engine = create_engine(db_connection)
            with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
                try:
                    conn.execute(text(f'CALL {procedure_name}();'))
                    logger.info(f"🚀 Ejecuta SP con nombre:{procedure_name} )")
        
                except Exception as e:
                    logger.info(f"Error ejecutando SP, validar:{e} )")
