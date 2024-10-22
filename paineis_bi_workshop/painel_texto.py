import streamlit as st
import os

caminho_raiz = os.getcwd()

# Caminho para logo
logo_image = caminho_raiz+'/static/idp_logo.png'

st.set_page_config(
    page_title="Aula - Paineis BI",
    page_icon=logo_image,
    layout="wide"
)

# Cabeçalho
st.image(logo_image,caption='idp', width=100)

st.title('Meu primeiro painél de BI :sunglasses:')
st.markdown('---')

#Diferentes tamanhos de texto
st.header('Isso é um cabeçalho')
st.subheader('Isso é um subcabeçalho')
st.text('Isso é um texto normal')

#formatação
st.markdown('Texto em **negrito** ou _itálico_')
st.markdown('[Isso é um texto com link](https://www.idp.edu.br/)',False)