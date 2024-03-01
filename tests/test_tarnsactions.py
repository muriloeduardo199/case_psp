from datetime import date
from main.main import Transaction, process_transaction, list_transactions, get_balance
import pytest
from faker import Faker


def test_process_transaction():
    # Criando um objeto Faker
    fake = Faker()
    fake_id = fake.unique.random_number(digits=5)
    # Criando uma transação de teste
    transaction = Transaction(
        amount = 100,
        description = 'Test transaction',
        payment_method = 'debit_card',
        card_number ='6543210987654321',  # Gerando um número de cartão de crédito falso
        card_holder_name = 'teste',  # Gerando um nome falso
        card_expiration_date = date(2024, 11, 30),  # Gerando uma data de validade falsa
        card_cvv = '123'  # Gerando um código de segurança falso
    )

    # Processando a transação
    payable = process_transaction(transaction)

    # Verificando se o payable foi criado corretamente
    assert fake_id == fake_id
    assert payable.status == 'paid'
    assert payable.payment_date == date.today()
    assert payable.fee == 3
    assert payable.amount == 97
