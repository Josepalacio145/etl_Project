def clean_dataframe(df):
    
    # Guardar el contenido original de 'Dep_no' si existe
    if 'COD_DPTO_N' in df.columns:
        dep_no_original = df['COD_DPTO_N'].astype(str)  # Convertir a string para preservar ceros

    # Limpiar nombres de columnas
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df = df.dropna(how="all")

    # Restaurar 'dep_no' si fue guardado
    if 'COD_DPTO_N' in df.columns and 'dep_no_original' in locals():
        df['cod_dpto_n'] = dep_no_original

    return df

