import pandas as pd


dados = pd.read_csv('dados/dados_tic.csv')
# dados['municipio'].head()
linha = dados[dados['municipio']=='Planaltina'].head()
print(type(linha), type(dados))