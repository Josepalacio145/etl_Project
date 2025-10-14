import yaml
from etl.extractor import read_excels
from etl.transform import clean_dataframe
from etl.loader import load_to_postgres
from etl.utils import move_file_to_processed
from etl.logger import get_logger
from etl.loaddata import call_stored_procedure
from etl.reviewdata import consultar_tblmaternas_mt


logger = get_logger("main")

def main():
    try:
        with open("config/settings.yaml") as f:
            config = yaml.safe_load(f)

        logger.info("🚀 Iniciando ETL...")
        logger.info("🚀 Limpia datos de staging_maternas u tbl_maternas_mt...")
        consultar_tblmaternas_mt( config["db_connection"],  "truncate table tbl_maternas_mt;",tipo=False)
        consultar_tblmaternas_mt( config["db_connection"],  "truncate table staging_maternas;",tipo=False) 


        files = read_excels(config["input_dir"])
        for name, file_data in files.items():
            df = clean_dataframe(file_data["df"])  # DataFrame real
            load_to_postgres(df, config["table_name"], config["db_connection"])

            # movemos archivo después de cargar
            move_file_to_processed(file_data["path"])

        logger.info("✅ ETL finalizado correctamente")
        # Llamada al procedimiento almacenado para carga a tabla final
       
        #consultar_tblmaternas_mt(config["db_connection"], "call public.sp_maternas_mt();",tipo=False)
        call_stored_procedure(config["db_connection"], "public.actualizar_departamentos")
        call_stored_procedure(config["db_connection"], "public.sp_maternas_mt")
        logger.info("✅ Procesar SP Maternas_MT")

        logger.info("🚀 Llamado a modelo")
        # Cargar modelo de árbol de decisión
        f
        logger.info("✅ Modelo de árbol de decisión generado correctamente")




    except Exception as e:
        logger.critical(f"Fallo inesperado en el ETL: {e}", exc_info=True)

if __name__ == "__main__":
    main()