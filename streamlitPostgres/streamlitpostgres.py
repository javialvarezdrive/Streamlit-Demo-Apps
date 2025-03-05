import streamlit as st
import pandas as pd
import sqlalchemy as sa
import plotly.express as px

# Configurar Streamlit
st.set_page_config(
    page_title="Dashboard - Gestión de Gimnasio",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para cargar los datos de la base de datos
@st.cache_data(ttl=600)
def cargarDatos(query):
    conString = st.secrets["conString"]
    engine = sa.create_engine(conString)
    df = pd.read_sql_query(query, engine)
    return df

# Función para ejecutar comandos SQL (si es necesario)
def ejecutarComandos(query):
    conString = st.secrets["conString"]
    engine = sa.create_engine(conString)
    engine.execute(query)

# Consultas para obtener datos desde las tablas
query_usuarios = 'SELECT * FROM public.users'
query_actividades = 'SELECT * FROM public.activities'
query_participantes = 'SELECT * FROM public.activity_participants'

# Cargar los datos
df_usuarios = cargarDatos(query_usuarios)
df_actividades = cargarDatos(query_actividades)
df_participantes = cargarDatos(query_participantes)

# Mostrar los datos en Streamlit
st.title('Dashboard - Gestión de Gimnasio')

# Miembros activos
miembros_activos = df_usuarios[df_usuarios['is_monitor'] == False]
total_miembros = len(miembros_activos)

# Actividades por realizar
actividades_proximas = df_actividades[df_actividades['date'] >= pd.to_datetime('today')]

# Participantes en actividades
participantes = df_participantes[df_participantes['attendance_status'] == 'Registered']
total_participantes = len(participantes)

# Mostrar las estadísticas generales
stats = [
    {"label": "Miembros Activos", "value": total_miembros},
    {"label": "Actividades por Realizar", "value": len(actividades_proximas)},
    {"label": "Total Participantes Registrados", "value": total_participantes}
]

for stat in stats:
    st.metric(label=stat["label"], value=stat["value"])

# Gráfico de actividades
fig_actividades = px.bar(
    actividades_proximas.sort_values(by='date'),
    x='name',
    y='date',
    title='Actividades Próximas'
)
st.plotly_chart(fig_actividades, use_container_width=True)

# Gráfico de distribución de participación
participacion_count = participantes['activity_id'].value_counts()
df_participacion = pd.DataFrame({
    'Actividad': participacion_count.index,
    'Participantes': participacion_count.values
})

fig_participacion = px.pie(
    df_participacion,
    names='Actividad',
    values='Participantes',
    title='Distribución de Participación por Actividad'
)
st.plotly_chart(fig_participacion, use_container_width=True)

# Mostrar los datos en tablas
st.subheader("Tabla de Miembros Activos")
st.dataframe(df_usuarios)

st.subheader("Tabla de Actividades")
st.dataframe(df_actividades)

st.subheader("Tabla de Participantes")
st.dataframe(df_participantes)
