
# Definindo alguns testes unitários para verificar o funcionamento do serviço
import pytest
from datetime import date, timedelta
from pydantic import  ValidationError
from main.main import Transaction, process_transaction, list_transactions, get_balance

def test_process_transaction():
    # Crie um objeto Transaction com os dados de teste
    transaction = Transaction(
        amount = 1000,
        description = "Compra online",
        payment_method = "debit_card",
        card_number = "1234567890123456",
        card_holder_name = "João",
        card_expiration_date = date(2024, 12, 31),
        card_cvv = "123"
    )

    # Chame a função process_transaction e armazene o resultado
    payable = process_transaction(transaction)

    # Verifique se o payable tem os atributos esperados
    assert payable.transaction_id == 1
    assert payable.status == "waiting_funds"
    assert payable.payment_date == date.today() + timedelta(days=30)
    assert payable.fee == 50
    assert payable.amount == 950



def test_list_transactions():
    # Chame a função list_transactions e armazene o resultado
    transactions = list_transactions()

    # Verifique se a lista de transações tem o tamanho esperado
    assert len(transactions) == 1

    # Verifique se a transação tem os atributos esperados
    assert transactions[0].amount == 1000
    assert transactions[0].description == "Compra online"
    assert transactions[0].payment_method == "credit_card"
    assert transactions[0].card_number == "1234567890123456"
    assert transactions[0].card_holder_name == "João Silva"
    assert transactions[0].card_expiration_date == date(2024, 12, 31)
    assert transactions[0].card_cvv == "123"

def test_get_balance():
    # Chame a função get_balance e armazene o resultado
    balance = get_balance()

    # Verifique se o saldo tem as chaves esperadas
    assert "available" in balance
    assert "waiting_funds" in balance

    # Verifique se o saldo tem os valores esperados
    assert balance["available"] == 0
    assert balance["waiting_funds"] == 950

