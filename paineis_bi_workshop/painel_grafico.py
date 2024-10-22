import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
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

st.subheader('Data Table')
st.write(dados.head())

st.title('População e Acesso aos Serviços de Comunicação Multimídia (SCM)')

# Line Plot
st.subheader('Gŕafico de Linha')
fig1 = plt.figure(figsize=(10, 6))
plt.plot(dados['municipio'], dados.sort_values('POP_TOT')['POP_TOT'], marker='o', label='População')
plt.plot(dados['municipio'], dados.sort_values('POP_TOT')['Acesso_SCM'], marker='s', label='Acesso a SCM')
plt.xlabel('Município')
plt.ylabel('Contagem')
#plt.title('Population and Access to SCM by Municipality')
plt.xticks(rotation=90)
plt.legend()
st.pyplot(fig1)


st.subheader('Gŕafico de Linha - Proporção')
fig2 = plt.figure(figsize=(10, 6))

acesso = dados.sort_values('POP_TOT')['Acesso_SCM']
pop = dados.sort_values('POP_TOT')['POP_TOT']

prop = acesso/pop

plt.plot(dados['municipio'], dados.sort_values('POP_TOT')['POP_TOT'], marker='o', label='População')
plt.plot(dados['municipio'], dados.sort_values('POP_TOT')['Acesso_SCM'], marker='s', label='Acesso a SCM')
plt.plot(dados['municipio'], prop*100000, marker='s', label='Proporção de acesso')
plt.xlabel('Município')
plt.ylabel('Contagem')
#plt.title('Population and Access to SCM by Municipality')
plt.xticks(rotation=90)
plt.legend()
st.pyplot(fig2)