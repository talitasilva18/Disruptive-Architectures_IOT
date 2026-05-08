# Pipeline de Dados IoT

Projeto utilizando Python, Docker, PostgreSQL e Streamlit para análise de dados IoT.

Instalação:

Criar ambiente virtual:
python -m venv venv

Ativar ambiente virtual:
.\venv\Scripts\Activate.ps1

Instalar bibliotecas:
pip install pandas psycopg2-binary sqlalchemy streamlit plotly

Docker PostgreSQL:

Criar banco PostgreSQL:

docker run --name postgres-iot 
-e POSTGRES_PASSWORD=admin123 
-e POSTGRES_USER=postgres 
-e POSTGRES_DB=iotdb 
-p 5432:5432 
-d postgres

Executar Projeto:

python -m src.load_data
python -m src.create_views
python -m streamlit run dashboard.py

# Caso seja necessário resetar as views SQL
python -m src.reset_views
