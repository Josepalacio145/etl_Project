import pandas as pd
from sqlalchemy import create_engine,text


#Funcion
def consultar_tblmaternas_mt(db_connection: str, consulta:str,tipo:bool=True) -> pd.DataFrame:
    """
    Consulta query a la tabla tblmaternas_mt y devuelve un DataFrame de pandas.
    
    Args:
        db_connection (str): Cadena de conexión a la base de datos.
        consulta (str): Consulta SQL a ejecutar.
        tipo (bool): Si es True, devuelve el DataFrame con los datos consultados. Si es False, no devuelve nada.
        
    Returns:
        pd.DataFrame: DataFrame que contiene los registros de la tabla tblmaternas_mt.
    """
    # Crear la conexión a la base de datos
    engine = create_engine(db_connection)
    
    # Definir la consulta SQL
    str_query = consulta
    
    # Ejecutar la consulta y cargar los resultados en un DataFrame
    with engine.connect() as connection:
        if tipo:
            df = pd.read_sql(str_query, connection)
            return df
        else:
            connection.execute(text(str_query))
    
