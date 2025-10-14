# Proyecto ETL con Arquitectura Limpia

## 📂 Estructura del Proyecto
```
/ETL_PROJECT/
│
├── config/           # Archivo de configuración "variables de entorno"
│   └── settings.yaml
├── data/             # archivos xlsx de entrada (datos de prueba)
│   ├── input_excels/ # Entrada de archivos a cargar
│   └── processed/    # Archivos ya cargado
├── etl/              # Scripts de Extracción, Transformación y Carga
│   ├── extractor.py  # Extracción de datos 
│   ├── loader.py     # Cargar los datos a la DB
│   ├── logger.py     # Control de logs de ejecución
│   ├── transform.py  # Transformar ó manipular datos
│   ├── reviewdata.py   
│   ├── utils.py      # Tiene la tarea de mover cada archivo ".xlsx" ya precargado en la Db
│   └── __init__.py
├── logs/             # Logs de errores, ejecución, validaciones
├── README.md         # Explicación general del proyecto
├── requirements.txt  # Librerías usadas
├── model/
│   ├── model_arbol.py
└── main.py           # Script principal para correr el ETL
```
    
## ⚙️ Requisitos Previos
Asegúrate de tener instalado:

```
Python
PostgreSQL.
```

## 🛠️ Instalación de librerias del proyecto
Desde la raiz del proyecto, ejecuta el siguiente comando:

```
pip install -r requirements.txt
```

## 🛠️ Ejecutar proyecto
Desde la raiz del proyecto, ejecuta el siguiente comando:

```
python main.py
```
## Agradecimientos a Juan C. Valdes por su apoyo y orientacion
## Dasborad para ejecutar tablero 
streamlit run etl/dashboard_mt.py
