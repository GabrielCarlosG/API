# Salva no banco as informações da API
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
# print(db_url) #teste para verificar se o DATABASE_URL não existisse

if not db_url:
    raise RuntimeError("A variável de ambiente DATABASE_URL não foi definida.")

try:
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            print(cur.fetchone())
        
except psycopg.errors.ConnectionTimeout as e:
    # Falha específica de tempo limite ao tentar conectar (psycopg 3)
    print(f"Tempo limite excedido ao conectar no PostgreSQL: {e}")

except psycopg.errors.InvalidPassword as e:
    # Erro específico de autenticação (SQLSTATE 28P01)
    print(f"Usuário ou senha inválidos na DATABASE_URL: {e}")

except psycopg.errors.InvalidCatalogName as e:
    # O banco de dados especificado na URL não existe (SQLSTATE 3D000)
    print(f"O banco de dados informado não existe: {e}")

except psycopg.OperationalError as e:
    # Outras falhas de conexão (ex: servidor fora do ar, DNS inválido, recusa de conexão)
    print(f"Falha operacional ou de rede ao conectar: {e}")

except psycopg.ProgrammingError as e:
    # Erros na query SQL (ex: erro de sintaxe, tabela inexistente)
    print(f"Erro na consulta SQL: {e}")

except psycopg.Error as e:
    # Qualquer outro erro mapeado pelo Psycopg (rede de segurança)
    print(f"Erro inesperado do Psycopg (SQLSTATE {e.sqlstate}): {e}")