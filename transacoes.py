# Importar bibliotecas necessárias
import datetime
import random
import hashlib

# Definir constantes para as taxas de processamento
FEE_DEBIT = 0.03 # 3% para transações com cartão de débito
FEE_CREDIT = 0.05 # 5% para transações com cartão de crédito

# Definir uma classe para representar uma transação
class Transaction:
    def __init__(self, amount, description, payment_method, card_number, card_holder, card_expiration, card_cvv):
        # Validar os dados da transação
        self.validate_data(amount, payment_method, card_number, card_holder, card_expiration, card_cvv)
        # Atribuir os atributos da transação
        self.id = random.randint(100000, 999999) # Gerar um id aleatório
        self.amount = amount # Valor da transação
        self.description = description # Descrição da transação
        self.payment_method = payment_method # Método de pagamento
        self.card_number = self.mask_card_number(card_number) # Número do cartão mascarado
        self.card_holder = card_holder # Nome do portador do cartão
        self.card_expiration = card_expiration # Data de validade do cartão
        self.card_cvv = card_cvv # Código de verificação do cartão
        self.created_at = datetime.datetime.now() # Data e hora da criação da transação
        self.payable = self.create_payable() # Recebível associado à transação

    # Método para validar os dados da transação
    def validate_data(self, amount, payment_method, card_number, card_holder, card_expiration, card_cvv):
        # Verificar se o valor da transação é positivo
        if amount <= 0:
            raise ValueError("O valor da transação deve ser positivo.")
        # Verificar se o método de pagamento é válido
        if payment_method not in ["debit_card", "credit_card"]:
            raise ValueError("O método de pagamento deve ser 'debit_card' ou 'credit_card'.")
        # Verificar se o número do cartão tem 16 dígitos
        if len(card_number) != 16 or not card_number.isdigit():
            raise ValueError("O número do cartão deve ter 16 dígitos.")
        # Verificar se o nome do portador do cartão não está vazio
        if not card_holder:
            raise ValueError("O nome do portador do cartão não pode ser vazio.")
        # Verificar se a data de validade do cartão está no formato MM/AA
        if len(card_expiration) != 5 or card_expiration[2] != "/":
            raise ValueError("A data de validade do cartão deve estar no formato MM/AA.")
        # Verificar se o mês e o ano da data de validade do cartão são válidos
        try:
            month = int(card_expiration[:2])
            year = int(card_expiration[3:])
            if month < 1 or month > 12:
                raise ValueError("O mês da data de validade do cartão deve estar entre 1 e 12.")
            if year < 0 or year > 99:
                raise ValueError("O ano da data de validade do cartão deve estar entre 0 e 99.")
        except ValueError:
            raise ValueError("A data de validade do cartão deve conter apenas números.")
        # Verificar se a data de validade do cartão não está expirada
        today = datetime.date.today()
        expiration_date = datetime.date(today.year + (year - today.year % 100), month, 1)
        if expiration_date < today.replace(day=1):
            raise ValueError("A data de validade do cartão está expirada.")
        # Verificar se o código de verificação do cartão tem 3 dígitos
        if len(card_cvv) != 3 or not card_cvv.isdigit():
            raise ValueError("O código de verificação do cartão deve ter 3 dígitos.")

    # Método para mascarar o número do cartão, deixando apenas os últimos 4 dígitos visíveis
    def mask_card_number(self, card_number):
        return "**** **** **** " + card_number[-4:]

    # Método para criar um recebível associado à transação
    def create_payable(self):
        # Calcular o valor líquido do recebível, descontando a taxa de processamento
        if self.payment_method == "debit_card":
            fee = FEE_DEBIT # 3% para transações com cartão de débito
            status = "paid" # Recebível pago
            payment_date = self.created_at # Data de pagamento = data da criação da transação (D+0)
        else:
            fee = FEE_CREDIT # 5% para transações com cartão de crédito
            status = "waiting_funds" # Recebível a receber
            payment_date = self.created_at + datetime.timedelta(days=30) # Data de pagamento = data da criação da transação + 30 dias (D+30)
        net_amount = round(self.amount * (1 - fee), 2) # Valor líquido do recebível, arredondado para duas casas decimais
        # Retornar um objeto do tipo Payable
        return Payable(self.id, net_amount, status, payment_date)

    # Método para retornar uma representação em string da transação
    def __str__(self):
        return f"Transação {self.id}: {self.description} - R${self.amount:.2f} - {self.payment_method} - {self.card_number} - {self.card_holder} - {self.card_expiration} - {self.card_cvv} - {self.created_at} - {self.payable}"

# Definir uma classe para representar um recebível
class Payable:
    def __init__(self, transaction_id, net_amount, status, payment_date):
        # Atribuir os atributos do recebível
        self.transaction_id = transaction_id # Id da transação associada
        self.net_amount = net_amount # Valor líquido do recebível
        self.status = status # Status do recebível
        self.payment_date = payment_date # Data de pagamento do recebível

    # Método para retornar uma representação em string do recebível
    def __str__(self):
        return f"Recebível da transação {self.transaction_id}: R${self.net_amount:.2f} - {self.status} - {self.payment_date}"

# Definir uma classe para representar um serviço de processamento de transações
class TransactionService:
    def __init__(self):
        # Inicializar uma lista vazia para armazenar as transações criadas
        self.transactions = []

    # Método para processar uma nova transação, recebendo os dados da transação como parâmetros
    def process_transaction(self, amount, description, payment_method, card_number, card_holder, card_expiration, card_cvv):
        # Criar um objeto do tipo Transaction com os dados da transação
        transaction = Transaction(amount, description, payment_method, card_number, card_holder, card_expiration, card_cvv)
        # Adicionar a transação à lista de transações
        self.transactions.append(transaction)
        # Retornar a transação criada
        return transaction

    # Método para retornar uma lista das transações já criadas
    def get_transactions(self):
        return self.transactions

    # Método para consultar o saldo do cliente, retornando um dicionário com as informações de saldo disponível e a receber
    def get_balance(self):
        # Inicializar as variáveis para armazenar os valores de saldo disponível e a receber
        available = 0
        waiting_funds = 0
        # Percorrer as transações criadas
        for transaction in self.transactions:
            # Se o recebível da transação estiver pago, somar o valor líquido ao saldo disponível
            if transaction.payable.status == "paid":
                available += transaction.payable.net_amount
            # Se o recebível da transação estiver a receber, somar o valor líquido ao saldo a receber
            elif transaction.payable.status == "waiting_funds":
                waiting_funds += transaction.payable.net_amount
        # Retornar um dicionário com as informações de saldo disponível e a receber
        return {"available": available, "waiting_funds": waiting_funds}

# Criar um objeto do tipo TransactionService
service = TransactionService()

# Processar algumas transações de exemplo
service.process_transaction(100, "Compra online", "credit_card", "1234567890123456", "João Silva", "12/24", "123")
service.process_transaction(50, "Pagamento de conta", "debit_card", "9876543210987654", "Maria Santos", "06/24", "456")
print(service.get_balance())