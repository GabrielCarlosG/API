# Salva no banco as informações da API
import os, sys
import psycopg
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
# print(db_url) #teste para verificar se o DATABASE_URL não existisse

if not db_url:
    raise RuntimeError("A variável de ambiente DATABASE_URL não foi definida.")

def conectar(db):
    with psycopg.connect(db,hostaddr="127.0.0.1",
                             connect_timeout=30,) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                print(cur.fetchone())

def get_connection(db) -> psycopg.Connection:
    with psycopg.connect(db,hostaddr="127.0.0.1",
                                 connect_timeout=30,) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1;")
                    print(cur.fetchone())
    return conn

try:
    get_connection(db_url)
        
except psycopg.errors.ConnectionTimeout as e:
    # Falha específica de tempo limite ao tentar conectar (psycopg 3)
    print(f"Tempo limite excedido ao conectar no PostgreSQL: {e}")
    sys.exit(1)

except psycopg.errors.UndefinedTable as e:
    # Erro específico de tabela inexistente (SQLSTATE 42P01)
    print(f"Tabela não existe: {e}")
    sys.exit(1)

except psycopg.OperationalError as e:
    # Outras falhas de conexão (ex: servidor fora do ar, DNS inválido, recusa de conexão)
    print(f"Verifique as informações de conexão: {e}")
    sys.exit(1)

except psycopg.Error as e:
    # Qualquer outro erro mapeado pelo Psycopg
    print(type(e).__name__)
    print(f"Erro inesperado do Psycopg (SQLSTATE {e.sqlstate}): {e}")
    sys.exit(1)