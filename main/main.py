from datetime import date, timedelta
from typing import List
from db.database import *
from validate.validator import *



def process_transaction(transaction: Transaction) -> Payable:
    """
    Processa uma transação e cria um payable associado.

    Args:
        transaction (Transaction): A transação a ser processada.

    Returns:
        Payable: O payable criado a partir da transação.
    """
    
    # Inserindo a transação na tabela de transações
    cur.execute("""
        INSERT INTO transactions (amount, description, payment_method, card_number, card_holder_name, card_expiration_date, card_cvv)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (transaction.amount, transaction.description, transaction.payment_method, transaction.card_number, transaction.card_holder_name, transaction.card_expiration_date, transaction.card_cvv))
    transaction_id = cur.fetchone()[0]
    conn.commit()

    if transaction.payment_method == 'debit_card':
        status = 'paid'
        payment_date = date.today()
        fee = int(transaction.amount * 0.03)
    else:
        status = 'waiting_funds'
        payment_date = date.today() + timedelta(days=30)
        fee = int(transaction.amount * 0.05)
    amount = transaction.amount - fee

   
    payable = Payable(
        transaction_id = transaction_id,
        status = status,
        payment_date = payment_date,
        fee = fee,
        amount = amount
    )

    # Inserindo o payable na tabela de payables
    cur.execute("""
        INSERT INTO payables (transaction_id, status, payment_date, fee, amount)
        VALUES (%s, %s, %s, %s, %s)
    """, (payable.transaction_id, payable.status, payable.payment_date, payable.fee, payable.amount))
    conn.commit()

   
    return payable


def list_transactions() -> List[Transaction]:

    """
    Retorna uma lista de todas as transações já criadas.

    Returns:
        List[Transaction]: A lista de transações.
    """
    # Selecionando todas as transações da tabela de transações
    cur.execute("""
        SELECT id, amount, description, payment_method, card_number, card_holder_name, card_expiration_date, card_cvv
        FROM transactions
    """)
    rows = cur.fetchall()

    
    transactions = []
    for row in rows:
        transaction = Transaction(
            amount = row[1],
            description = row[2],
            payment_method = row[3],
            card_number = row[4],
            card_holder_name = row[5],
            card_expiration_date = row[6],
            card_cvv = row[7]
        )
        transactions.append(transaction)

    
    return transactions


def get_balance() -> dict:
    """
    Retorna o saldo do cliente, incluindo o saldo disponível e a receber.

    Returns:
        dict: Um dicionário contendo o saldo disponível e a receber do cliente.
    """
    # Selecionando o saldo disponível e a receber do cliente da tabela de payables
    cur.execute("""
        SELECT status, SUM(amount)
        FROM payables
        GROUP BY status
    """)
    rows = cur.fetchall()

    # Criando um dicionário com as informações do saldo
    balance = {}
    for row in rows:
        if row[0] == 'paid':
            balance['available'] = row[1]
        else:
            balance['waiting_funds'] = row[1]

    # Retornando o saldo do cliente
    return balance



