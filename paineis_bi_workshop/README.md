# Workshop - Utilizando Pandas na Prática - Painéis de Dados

![logo](/static/idp_logo.png)

**Professor:** Lucas dos Santos Althoff
**Data:** 20/04/2024

---

Repositório para Workshop de Data Science para Negócios II. Este repositório contém dados e exemplos de códigos utilizados no workshop.


## Dados

Os dados a serem utilizados no workshop são: 

- `dados/estoque.csv` (Dados falsos de estoque)
- `dados/dados_tic.csv` (Dados reais da Região do Entorno do DF - RIDE)

## Dependências

Para criar um ambiente com todas as dependências usando o Conda:

`conda env create -f environment.yml`

Caso você não utilize Conda utilize execute o seguinte código no terminal para configurar seu ambiente: 

`pip install -r requirements.txt`

## Executando

Para executar os painéis do Workshop basta executar o seguinte comando em seu terminal:

`streamlit run painel_estoque.py`

ou

`python -m streamlit run painel_texto.py`

# Passo a passo (github)

1) git clone `https://github.com/lucas-althoff/paineis_bi_workshop.git`
2) Abrir VS Code
3) Abrir a pasta File>Open Folder>workshop_paineis_streamlit-1
4) Instalar bibliotecas
   1) Abrir terminal em: Terminal>New Terminal
   2) Executar no terminal esse código: `pip install -r requirements.txt`
5) Executar os exemplos 
   `python -m streamlit run painel_texto.py`

# Passo a passo (instalação local)

1) Instalar VS Code
2) Instalar Python
3) Baixar arquivo `workshop_paineis_streamlit-1.zip` no ambiente virtual 
   1) https://ambientevirtual.idp.edu.br/
4) Descomprimir o arquivo `workshop_paineis_streamlit-1.zip`
5) Abrir VS Code
6) Abrir a pasta File>Open Folder>workshop_paineis_streamlit-1
7) Instalar bibliotecas
   1) Abrir terminal em: Terminal>New Terminal
   2) Executar no terminal esse código: `pip install -r requirements.txt`
8) Executar um exemplo 
   `python -m streamlit run painel_texto.py`



---

# Kaggle

1) Instalar client api kaggle: `pip install Kaggle`
2) Instalar pydantic-settings: `pip install pydantic-settings`
3) Entrar no site www.kaggle.com > Cadastrar no site > Settings > API > Create New Token
4) Criar .env
5) Copiar informações para .env
6) Opcional: criar um arquivo .gitignore e adicionar o .env
6) Carregar configurações na variavel settings
7) Rodar código `streamlit run paneinel_kaggle.py`

# Tarefa de casa
8) Incluir gráficos no painel e modificar Titulo incluindo seu nome
9) Utilizar como referência o [repositório git](https://github.com/FedeCaprari/Ukraine-Missile-Interception-Dashboard/blob/main/Ukraine_graph_generator.py)