import psycopg2
import os
from dotenv import load_dotenv
# Conectando ao banco de dados postgres
load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
cur = conn.cursor()

# Criando as tabelas de transações e payables
cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        amount INTEGER NOT NULL,
        description VARCHAR(255) NOT NULL,
        payment_method VARCHAR(10) NOT NULL,
        card_number VARCHAR(16) NOT NULL,
        card_holder_name VARCHAR(255) NOT NULL,
        card_expiration_date DATE NOT NULL,
        card_cvv VARCHAR(3) NOT NULL
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS payables (
        id SERIAL PRIMARY KEY,
        transaction_id INTEGER NOT NULL REFERENCES transactions(id),
        status VARCHAR(10) NOT NULL,
        payment_date DATE NOT NULL,
        fee INTEGER NOT NULL,
        amount INTEGER NOT NULL
    )
""")

conn.commit()