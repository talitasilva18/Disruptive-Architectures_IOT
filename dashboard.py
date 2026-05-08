import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from src.config import DATABASE_URL


# Conexão com PostgreSQL
engine = create_engine(DATABASE_URL)


# Função para carregar dados das views
def load_data(view_name):
    query = f"SELECT * FROM {view_name}"
    return pd.read_sql(query, engine)


# Configuração da página
st.set_page_config(
    page_title="Pipeline IoT Dashboard",
    layout="wide"
)

# Título principal
st.title("Pipeline de Dados IoT com PostgreSQL e Streamlit")

st.write(
    "Análise de leituras de temperatura coletadas por dispositivos IoT."
)

st.divider()


# =========================
# GRÁFICO 1
# =========================

st.subheader("1. Média de Temperatura por Ambiente")

df_avg = load_data("avg_temp_por_dispositivo")

fig1 = px.bar(
    df_avg,
    x="location_type",
    y="avg_temp",
    color="location_type",
    text="avg_temp",
    title="Média de Temperatura por Ambiente",
    labels={
        "location_type": "Ambiente",
        "avg_temp": "Temperatura Média (°C)"
    },
    template="plotly_dark"
)

fig1.update_traces(
    textposition="outside"
)

fig1.update_layout(
    xaxis_title="Ambiente",
    yaxis_title="Temperatura Média",
    showlegend=False,
    font=dict(size=16)
)

st.plotly_chart(fig1, use_container_width=True)

st.divider()


# =========================
# GRÁFICO 2
# =========================

st.subheader("2. Quantidade de Leituras por Hora")

df_hora = load_data("leituras_por_hora")

fig2 = px.line(
    df_hora,
    x="hora",
    y="contagem",
    markers=True,
    title="Leituras por Hora do Dia",
    labels={
        "hora": "Hora do Dia",
        "contagem": "Quantidade de Leituras"
    },
    template="plotly_dark"
)

fig2.update_layout(
    xaxis_title="Hora do Dia",
    yaxis_title="Quantidade de Leituras",
    font=dict(size=16)
)

fig2.update_traces(
    line=dict(width=4)
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()


# =========================
# GRÁFICO 3
# =========================

st.subheader("3. Temperaturas Máximas e Mínimas por Dia")

df_temp = load_data("temp_max_min_por_dia")

df_temp["data"] = pd.to_datetime(df_temp["data"])

fig3 = px.line(
    df_temp,
    x="data",
    y=["temp_max", "temp_min"],
    markers=True,
    title="Temperaturas Máximas e Mínimas por Dia",
    labels={
        "data": "Data",
        "value": "Temperatura",
        "variable": "Tipo"
    },
    template="plotly_dark"
)

fig3.update_layout(
    xaxis_title="Data",
    yaxis_title="Temperatura",
    legend_title="Tipo",
    font=dict(size=16)
)

fig3.update_traces(
    line=dict(width=3)
)

st.plotly_chart(fig3, use_container_width=True)

st.divider()


# =========================
# MÉTRICAS EXTRAS
# =========================

st.subheader("Resumo Geral")

col1, col2 = st.columns(2)

temp_in = df_avg[df_avg["location_type"] == "In"]["avg_temp"].values
temp_out = df_avg[df_avg["location_type"] == "Out"]["avg_temp"].values

if len(temp_in) > 0:
    col1.metric(
        "Temperatura Média Interna",
        f"{temp_in[0]} °C"
    )

if len(temp_out) > 0:
    col2.metric(
        "Temperatura Média Externa",
        f"{temp_out[0]} °C"
    )