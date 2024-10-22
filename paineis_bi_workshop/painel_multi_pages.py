import streamlit as st
import os
import pandas as pd

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
    # Diferentes tamanhos de texto
    st.title('Painel Cidades Inteligentes')

    dados = pd.read_csv('dados/dados_tic.csv')

    st.subheader('Tabela de Dados')
    informacao = dados[['municipio','POP_TOT']]

    st.write(informacao)

def page3():
    import matplotlib.pyplot as plt 
    dados = pd.read_csv('dados/dados_tic.csv')

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
    plt.style.use('dark_background')
    st.pyplot(fig1)

def page4():
    import matplotlib.pyplot as plt
    dados = pd.read_csv('dados/dados_tic.csv')

    st.subheader('Gŕafico de Linha - Proporção')
    fig2 = plt.figure(figsize=(10, 6))

    acesso = dados.sort_values('POP_TOT')['Acesso_SCM']
    pop = dados.sort_values('POP_TOT')['POP_TOT']

    prop = acesso/pop
    prop = prop.sort_values()

    # plt.plot(dados['municipio'], dados.sort_values('POP_TOT')['POP_TOT'], marker='o', label='População')
    # plt.plot(dados['municipio'], dados.sort_values('POP_TOT')['Acesso_SCM'], marker='s', label='Acesso a SCM')
    plt.plot(dados['municipio'], prop*100000, marker='s', label='Proporção de acesso')
    plt.xlabel('Município')
    plt.ylabel('Contagem')
    #plt.title('Population and Access to SCM by Municipality')
    plt.xticks(rotation=90)
    plt.legend()
    plt.style.use('dark_background')
    st.pyplot(fig2)

# Dicionario contedo paginas e suas funções
page_names_to_funcs = {
    "Raiz": main_page,
    "Municipios": page2,
    "Gráfico de acessos SCM": page3,
    "Gráfico de proporção SCM": page4
}

selected_page = st.sidebar.selectbox("Selecione a página", page_names_to_funcs.keys())
print(selected_page)
page_names_to_funcs[selected_page]()