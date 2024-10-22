import streamlit as st
import pandas as pd
import os

# Cabeçalho
caminho_raiz = os.getcwd()

# Caminho para logo
logo_image = caminho_raiz+'/static/idp_logo.png'

st.set_page_config(
    page_title="Workshop - Paineis BI",
    page_icon=logo_image,
    layout="wide"
)

st.image(logo_image,caption='', width=100)
st.markdown('---')
# Fim cabeçalho

# Diferentes tamanhos de texto
st.title('Painel Cidades Inteligentes')

dados = pd.read_csv('dados/dados_tic.csv')

st.subheader('Tabela de Dados')

#TODO: Incluir filtro interativo para selecionar municipio
# list(dados['municipio'])
# st.sidebar.selectbox()

informacao = dados[['municipio','POP_TOT']]

st.write(dados.head())