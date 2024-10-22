import streamlit as st
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

st.title('Workshop - Painél BI')
st.markdown('---')

# Fim do cabeçalho



def main_page():
    st.title('Meu primeiro painél de BI :sunglasses:')

    #Diferentes tamanhos de texto
    st.header('Isso é um cabeçalho')
    st.subheader('Isso é um subcabeçalho')
    st.text('Isso é um texto normal')

    #formatação
    st.markdown('Texto em **negrito** ou _itálico_')
    st.markdown('[Isso é um texto com link](https://www.idp.edu.br/)',False)

def page2():
    st.markdown("# Painel 2 ❄️")
    st.sidebar.markdown("# Painel 2 ❄️")

def page3():
    st.markdown("# Painel 3 🎉")
    st.sidebar.markdown("# Painel 3 🎉")

# Dicionario contedo paginas e suas funções
page_names_to_funcs = {
    "Raiz": main_page,
    "Painel 2": page2,
    "Painel 3": page3,
}

selected_page = st.sidebar.selectbox("Selecione a página", page_names_to_funcs.keys())
print(selected_page)
page_names_to_funcs[selected_page]()