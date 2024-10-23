from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
from usatoken import configuracoes
import os
import streamlit as st
import plotly.express as px


def download_dataset():
    # Kaggle API client
    api = KaggleApi()
    
    # Autenticar utilizando token
    api.set_config_value('username', configuracoes.kaggle_username)
    api.set_config_value('key', configuracoes.kaggle_key)
    api.authenticate()
    
    # Definir um dataset e um caminho de onde baixar os dados
    dataset = 'piterfm/massive-missile-attacks-on-ukraine'
    path = './dados'

    # Download the dataset
    api.dataset_download_files(dataset, path=path, unzip=True)
    st.success(f"Dataset {dataset} baixado com sucesso!")


def process_dataset(data):
    # Drop unnecessary columns including the original 'time_end'
    data.drop(columns=['time_end', 'model', 'launch_place', 'target', 'destroyed_details', 'carrier', 'source'], inplace=True)
    
    # Ensure that time is removed and only the date is kept
    data['time_start'] = data['time_start'].astype(str).apply(lambda x: x.split(' ')[0])
    
    # Rename 'time_start' to 'date'
    data.rename(columns={'time_start': 'date'}, inplace=True)

    # Convert 'date' to datetime object and extract the date part
    data['date'] = pd.to_datetime(data['date']).dt.date

    return data


def monthly_interception_rate(data):
    # Convert 'date' to datetime object for proper resampling
    data['date'] = pd.to_datetime(data['date'])
    # Group by month and sum the values of 'launched' and 'destroyed'
    monthly_data = data.resample('M', on='date').sum().reset_index()
    
    # Calculate the interception rate based on monthly sums
    monthly_data['interception_rate'] = (monthly_data['destroyed'] / monthly_data['launched'] * 100).fillna(0).round(0).astype(int)
    monthly_data['interception_rate'] = monthly_data['interception_rate'].astype(str) + '%'
    
    # Format date to show only year and month for readability in the chart
    monthly_data['date'] = monthly_data['date'].dt.strftime('%Y-%m')
    
    return monthly_data


def plot_data(data):
    fig = px.bar(data, x='date', y=['launched', 'destroyed'],
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
            rangeslider=dict(visible=True),  # Habilita o seletor de intervalo
            type='date'  # Garante que o eixo X seja tratado como data
        ),
        yaxis=dict(
            title_font=dict(size=20, color='black'),
            tickfont=dict(size=18, color='black'),
            range=[0, 110]
        )
    )
    return fig


def plot_interception_rate(data):
    fig = px.line(data, x='date', y='interception_rate', color_discrete_sequence=['darkblue'])
    fig.update_traces(line=dict(width=4))
    fig.update_layout(
        title='Taxa Média de Interceptação Mensal ao Longo do Tempo',
        xaxis_title='Mês',
        yaxis_title='Taxa de Interceptação (%)',
        xaxis=dict(
            title_font=dict(size=18, color='black'),
            tickfont=dict(size=16, color='black'),
            tickangle=-90,
            tickmode='linear',
            dtick='M1',
            rangeslider=dict(visible=True),  # Habilita o seletor de intervalo
            type='date'  # Garante que o eixo X seja tratado como data
        ),
        yaxis=dict(
            title_font=dict(size=20, color='black'),
            tickfont=dict(size=18, color='black'),
            range=[50, 100]
        )
    )
    return fig



# Streamlit app
st.title('Análise de Lançamentos e Interceptações de Mísseis')

if st.sidebar.button('Download dos dados', type="primary"):
    download_dataset()
    data_path = os.path.join(os.getcwd(), 'dados/missile_attacks_daily.csv')
    
    if os.path.exists(data_path):
        data = pd.read_csv(data_path)
        data_processed = process_dataset(data.copy())
        
        st.subheader("Dados Processados")
        st.write(data_processed)
        
        st.subheader("Gráfico de Lançamentos vs Destruições")
        st.plotly_chart(plot_data(data_processed))
        
        st.subheader("Taxa de Interceptação Mensal")
        monthly_data = monthly_interception_rate(data_processed)
        st.plotly_chart(plot_interception_rate(monthly_data))
    else:
        st.error("O arquivo de dados não foi encontrado. Tente baixar os dados novamente.")
