from datetime import date, timedelta
from main.main import Transaction, process_transaction, list_transactions, get_balance
import pytest
from faker import Faker



def test_process_transaction():
    """
    Testa o processamento de transações com cartão de crédito.

    Esta função cria uma transação de teste usando dados fictícios e a processa.
    Ela verifica se o objeto 'payable' resultante possui as propriedades esperadas.

    Retorna:
        None
    """
    
    fake = Faker()
    fake_id = fake.unique.random_number(digits=5)
    
    transaction = Transaction(
        amount = 100,
        description = 'Test transaction',
        payment_method = 'debit_card',
        card_number ='6543210987654321',  
        card_holder_name = 'Murilo Eduardo',  
        card_expiration_date = date(2024, 11, 30),  
        card_cvv = '123'  
    )

    payable = process_transaction(transaction)

    assert fake_id == fake_id
    assert payable.status == 'paid'
    assert payable.payment_date == date.today()
    assert payable.fee == 3
    assert payable.amount == 97

def test_credit_process_transaction():
    """
    Testa o processamento de transações com cartão de crédito.

    Esta função cria uma transação de teste usando dados fictícios e a processa.
    Em seguida, verifica se o objeto 'payable' resultante possui as propriedades esperadas.

    Retorna:
        None
    """

    # Criando um objeto Faker
    fake = Faker()
    fake_id = fake.unique.random_number(digits=5)
    # Criando uma transação de teste
    transaction = Transaction(
        amount = 100,
        description = 'Test transaction',
        payment_method = 'credit_card',
        card_number ='6543210987654321',  # Gerando um número de cartão de crédito falso
        card_holder_name = 'Murilo Eduardo',  # Gerando um nome falso
        card_expiration_date = date(2024, 11, 30),  # Gerando uma data de validade falsa
        card_cvv = '123'  # Gerando um código de segurança falso
    )

    # Processando a transação
    payable = process_transaction(transaction)

    # Verificando se o payable foi criado corretamente
    assert fake_id == fake_id
    assert payable.status == 'waiting_funds'
    assert payable.payment_date ==  date.today() + timedelta(days=30)
    assert payable.fee == 5
    assert payable.amount == 95


@pytest.fixture
def example_transactions():
    """"Definindo uma fixture que cria uma lista de transações de exemplo"""
    
    transactions = [
        Transaction(
            amount = 100,
            description = "Compra online",
            payment_method = "credit_card",
            card_number = "1234-5678-9012-3456",
            card_holder_name = "João da Silva",
            card_expiration_date = "12/24",
            card_cvv = "123"
        ),
        Transaction(
            amount = 50,
            description = "Pagamento de conta",
            payment_method = "Boleto",
            card_number = None,
            card_holder_name = None,
            card_expiration_date = None,
            card_cvv = None
        )
    ]
    return transactions



def test_card_expiration_date_must_be_valid():
    """"Teste para verificar se a data de validade do cartão não está no passado"""
    
    with pytest.raises(ValueError, match="card_expiration_date must not be in the past"):
        Transaction(amount=100, description="Compra online", payment_method="credit_card",
                    card_number="1234567890123456", card_holder_name="João da Silva",
                    card_expiration_date=date(2020, 1, 1), card_cvv="123")
        


def test_valid_transaction_creation():
    """"Teste para verificar se a criação de uma transação válida não lança exceção"""
    
    transaction = Transaction(amount=100, description="Compra online", payment_method="credit_card",
                              card_number="1234567890123456", card_holder_name="João da Silva",
                              card_expiration_date=date(2024, 12, 31), card_cvv="123")
    assert transaction is not None



def test_list_transactions_returns_non_empty_list():
    """"Teste para verificar se a função list_transactions() retorna uma lista não vazia"""
    
    transactions = list_transactions()
    assert isinstance(transactions, list)
    assert len(transactions) > 0


def test_list_transactions_contains_valid_transactions():
    """"Teste para verificar se cada transação na lista é uma instância válida da classe Transaction"""
    
    transactions = list_transactions()
    for transaction in transactions:
        assert isinstance(transaction, Transaction)


def test_get_balance_returns_non_empty_dict():
    """"Teste para verificar se a função get_balance() retorna um dicionário não vazio"""
    
    balance = get_balance()
    assert isinstance(balance, dict)
    assert len(balance) > 0



def test_get_balance_contains_expected_keys():
    """Teste para verificar se as chaves 'available' e 'waiting_funds' estão presentes no dicionário"""
    balance = get_balance()
    assert 'available' in balance
    assert 'waiting_funds' in balance