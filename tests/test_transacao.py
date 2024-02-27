# Importar o módulo que contém o código a ser testado
import transacoes
import datetime
import random
# Importar o pytest
import pytest

# Criar uma função de teste para verificar se o construtor da classe Transaction é válido
def test_transaction_constructor():
    # Criar um objeto do tipo Transaction com dados válidos
    transaction = transacoes.Transaction(amount=100, description="Compra online", payment_method="credit_card", card_number="1234567890123456", card_holder="João Silva", card_expiration="12/24", card_cvv="123")
    # Verificar se o objeto é do tipo Transaction
    assert isinstance(transaction, transacoes.Transaction)
    # Verificar se o objeto tem os atributos esperados
    assert transaction.amount == 100
    assert transaction.description == "Compra online"
    assert transaction.payment_method == "credit_card"
    assert transaction.card_number == "**** **** **** 3456" # Verificar se o número do cartão foi mascarado
    assert transaction.card_holder == "João Silva"
    assert transaction.card_expiration == "12/24"
    assert transaction.card_cvv == "123"
    assert transaction.created_at.date() == datetime.date.today() # Verificar se a data da criação da transação é a data atual
    assert transaction.payable.transaction_id == transaction.id # Verificar se o recebível associado à transação tem o mesmo id da transação
