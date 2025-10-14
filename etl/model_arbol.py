import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import yaml
from etl.reviewdata import consultar_tblmaternas_mt
#from etl.logger import get_logger


with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)  
#logger = get_logger("model_arbol")

@st.cache_data
def load_data():
    
    try:
        df= consultar_tblmaternas_mt(config["db_connection"], "SELECT id_registro,fecha_evento,edad,rangos_edades,codigo_prestacion,nacionalidad,ocupacion,etnia,semanas,pais,departamento,municipio,causa,latitud,longitud FROM tbl_maternas_mt;",tipo=True)
        #df = pd.read_csv("data/data-1759093258628_total.csv")
        df['muerte'] = 1
        #logger.info("✅ Carga de datos exitosa")
        return df
    except Exception as e:
        e.error(f"Error cargando datos: {e}", exc_info=True)
        st.stop()   

def entrenar_modelo(df):
    features = ['departamento', 'etnia', 'ocupacion', 'edad', 'causa']
    df = df[features + ['muerte']].dropna()
    for col in features:
        df[col] = LabelEncoder().fit_transform(df[col].astype(str))
    X = df[features]
    y = df['muerte']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    clf = DecisionTreeClassifier(max_depth=5)
    clf.fit(X_train, y_train)
    return clf, features

def mostrar_arbol(modelo, features):
    fig, ax = plt.subplots(figsize=(20, 10))
    plot_tree(modelo, feature_names=features, class_names=['No Muerte', 'Muerte'], filled=True)
    st.pyplot(fig)

def mostrar_importancia(modelo, features):
    importancias = modelo.feature_importances_
    fig, ax = plt.subplots()
    sns.barplot(x=importancias, y=features, ax=ax)
    ax.set_title("Importancia de características")
    st.pyplot(fig)

st.title("Modelo de Predicción de Muerte Materna")
df = load_data()

if st.button("Entrenar modelo y mostrar visualizaciones"):
    #logger.info("🚀 Llamado a modelo")
    with st.spinner("Entrenando modelo..."):
        modelo, features = entrenar_modelo(df)
        st.subheader("Árbol de decisión")
    
    mostrar_arbol(modelo, features)
    from sklearn.metrics import accuracy_score
    y_pred = modelo.predict(df[features])
    st.metric("Precisión del modelo", f"{accuracy_score(df['muerte'], y_pred):.2f}")
    st.subheader("Importancia de características")
    mostrar_importancia(modelo, features) 