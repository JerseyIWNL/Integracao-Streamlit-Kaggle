import streamlit as st
import pandas as pd
import plotly.express as px
import os
import zipfile
import time

# Configurar variáveis de ambiente para as credenciais do Kaggle
os.environ['pedrojersey'] = st.secrets["kaggle"]["username"]
os.environ['9559362a527b372ed49d730071e3c7ca'] = st.secrets["kaggle"]["key"]

st.set_page_config(page_title= "Painel de Lançamentos vs Interceptações de Mísseis na Ucrânia", page_icon=":bar_chart:")

def baixar_dataset():
    # Inicializar o cliente da API do Kaggle e autenticar
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    
    # Definir o dataset e o caminho onde os arquivos serão baixados
    dataset = 'piterfm/massive-missile-attacks-on-ukraine'
    caminho = '.'

    # Baixar o arquivo zip do dataset
    api.dataset_download_files(dataset, path=caminho, unzip=False)

    # Definir o caminho do arquivo zip
    caminho_zip = os.path.join(caminho, dataset.split('/')[-1] + '.zip')

    # Extrair apenas o arquivo necessário
    with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
        # Obter a lista de todos os arquivos no zip
        nomes_arquivos = zip_ref.namelist()
        # Encontrar o arquivo necessário e extrair
        for arquivo in nomes_arquivos:
            if arquivo.endswith('missile_attacks_daily.csv'):
                zip_ref.extract(arquivo, caminho)
                # Opcionalmente, renomear e mover o arquivo para um local mais conveniente
                os.rename(os.path.join(caminho, arquivo), os.path.join(caminho, 'missile_attacks_daily.csv'))
                break

    # Limpar o arquivo zip após a extração
    os.remove(caminho_zip)

def remover_tempo(dados):
    # Garantir que o tempo seja removido e apenas a data seja mantida
    dados['time_start'] = dados['time_start'].astype(str).apply(lambda x: x.split(' ')[0])
    return dados

def processar_dataset(dados):
    # Remover colunas desnecessárias, incluindo 'time_end'
    dados.drop(columns=['time_end', 'model', 'launch_place', 'target', 'destroyed_details', 'carrier', 'source'], inplace=True)

    # Renomear 'time_start' para 'data'
    dados.rename(columns={'time_start': 'data'}, inplace=True)

    # Converter 'data' para objeto datetime e extrair a parte da data
    dados['data'] = pd.to_datetime(dados['data']).dt.date

    return dados

def agregar_dados(dados):
    # Agrupar os dados por data e somar os valores de 'launched' e 'destroyed'
    dados_diarios = dados.groupby('data').agg({
        'launched': 'sum',
        'destroyed': 'sum'
    }).reset_index()
    # Calcular a taxa de interceptação diária
    dados_diarios['taxa_interceptacao'] = (dados_diarios['destroyed'] / dados_diarios['launched'] * 100).fillna(0).round(0).astype(int)
    dados_diarios['taxa_interceptacao'] = dados_diarios['taxa_interceptacao'].astype(str) + '%'
    return dados_diarios

def taxa_interceptacao_mensal(dados):
    # Converter 'data' para objeto datetime para permitir o reamostramento correto
    dados['data'] = pd.to_datetime(dados['data'])
    # Agrupar por mês e somar os valores de 'launched' e 'destroyed'
    dados_mensais = dados.resample('M', on='data').sum().reset_index()
    # Calcular a taxa de interceptação com base nas somas mensais, arredondar e converter para string com '%'
    dados_mensais['taxa_interceptacao'] = (dados_mensais['destroyed'] / dados_mensais['launched'] * 100).fillna(0).round(0).astype(int)
    dados_mensais['taxa_interceptacao'] = dados_mensais['taxa_interceptacao'].astype(str) + '%'
    # Formatar a data para mostrar apenas ano e mês para maior legibilidade no gráfico
    dados_mensais['data'] = dados_mensais['data'].dt.strftime('%Y-%m')
    return dados_mensais

def plotar_dados(dados):
    fig = px.bar(dados, x='data', y=['launched', 'destroyed'],
                 labels={'value': 'Contagem', 'variable': 'Categoria'},
                 color_discrete_map={'launched': 'darkblue', 'destroyed': 'darkgray'},
                 barmode='group')
    fig.update_traces(marker_line_width=0)
    fig.update_layout(
        title='Mísseis Lançados vs Destruídos ao Longo do Tempo',
        xaxis_title='Data',
        yaxis_title='Número de Mísseis',
        xaxis=dict(
            title_font=dict(size=18, color='black'),
            tickfont=dict(size=16, color='black'),
            rangeslider=dict(visible=True),  # Ativar o controle deslizante de intervalo
            type='date'  # Garantir que o eixo X seja tratado como data
        ),
        yaxis=dict(
            title_font=dict(size=20, color='black'),
            tickfont=dict(size=18, color='black'),
            range=[0, 110]
        )
    )
    return fig

def plotar_taxa_interceptacao(dados):
    fig = px.line(dados, x='data', y='taxa_interceptacao', color_discrete_sequence=['darkblue'])
    fig.update_traces(line=dict(width=4))
    fig.update_layout(
        title='Taxa Média Mensal de Interceptação ao Longo do Tempo',
        xaxis_title='Mês',
        yaxis_title='Taxa de Interceptação (%)',
        xaxis=dict(
            title_font=dict(size=18, color='black'),
            tickfont=dict(size=16, color='black'),
            tickangle=-90,
            tickmode='linear',
            dtick='M1',
            rangeslider=dict(visible=True),  # Ativar o controle deslizante de intervalo
            type='date'  # Garantir que o eixo X seja tratado como data
        ),
        yaxis=dict(
            title_font=dict(size=20, color='black'),
            tickfont=dict(size=18, color='black'),
            range=[50, 100]
        )
    )
    return fig


# Interface do aplicativo Streamlit
st.title('Painel da Ucrânia')
st.subheader('Mísseis disparados, interceptados e taxa de interceptação')
placeholder = st.empty()

if 'data_loaded' not in st.session_state:
    st.session_state['data_loaded'] = False

if st.sidebar.button('Obter Dados', type="primary"):

    baixar_dataset()
    st.session_state['data_loaded'] = True

if not st.session_state['data_loaded']:
    st.markdown("Para começar, clique no botão 'OBTER DADOS' no painel à esquerda")
if st.session_state['data_loaded']:
    # Esse botão permitirá que os usuários baixem 'missile_attacks_daily.csv' quando disponível
    sucesso = st.success('Dados baixados e extraídos com sucesso!')
    time.sleep(2)  # Aguardar 2 segundos
    sucesso.empty()  # Limpar o alerta

    st.markdown(
        "_A base de dados está hospedada no Kaggle e é atualizada frequentemente. Você pode encontrar mais detalhes [aqui](https://www.kaggle.com/datasets/piterfm/massive-missile-attacks-on-ukraine)._",
        unsafe_allow_html=True
    )    
    with open("missile_attacks_daily.csv", "rb") as file:
        btn = st.sidebar.download_button(
            label="Exportar Dados",
            data=file,
            file_name="missile_attacks_daily.csv",
            mime="text/csv"
        )
    dados = pd.read_csv("missile_attacks_daily.csv")

    # Processar o dataset
    dados_processados = remover_tempo(dados.copy())  # Remover a parte do tempo
    dados_processados = processar_dataset(dados_processados)  # Processar o dataset
    dados_agregados = agregar_dados(dados_processados)  # Agregar os dados por dia

    data_mais_recente = dados_agregados['data'].max()
    data_mais_antiga = dados_agregados['data'].min()
    misseis_disparados_mais_recente = int(dados_agregados[dados_agregados['data'] == data_mais_recente]['launched'].sum())

    # Exibindo Seletores de Data
    st.sidebar.title("Escolha o Intervalo de Datas")
    data_inicio = st.sidebar.date_input("Data de Início", min_value=data_mais_antiga, max_value=data_mais_recente, value=data_mais_antiga)
    data_fim = st.sidebar.date_input("Data de Fim", min_value=data_mais_antiga, max_value=data_mais_recente, value=data_mais_recente)
    intervalo_datas = data_inicio <= dados_agregados['data']

    st.sidebar.metric(label="Mísseis disparados na última data", value=f"{misseis_disparados_mais_recente}")
    dados_intervalo = dados_agregados.query(f"'{data_inicio}' <= data <= '{data_fim}'")

    # Exibir gráficos de mísseis disparados vs interceptados
    st.plotly_chart(plotar_dados(dados_intervalo))

    # Dados mensais e exibir gráfico da taxa de interceptação
    dados_mensais = taxa_interceptacao_mensal(dados_processados)
    st.plotly_chart(plotar_taxa_interceptacao(dados_mensais))
