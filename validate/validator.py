from datetime import date
from pydantic import BaseModel, validator
from db.database import *


class Transaction(BaseModel):
    """
    Modelo de dados para uma transação.

    Campos:
        amount (int): O valor da transação.
        description (str): A descrição da transação.
        payment_method (str): O método de pagamento usado na transação.
        card_number (str): O número do cartão usado na transação.
        card_holder_name (str): O nome do titular do cartão.
        card_expiration_date (date): A data de validade do cartão.
        card_cvv (str): O código de segurança do cartão.
    """
    amount: int
    description: str
    payment_method: str
    card_number: str
    card_holder_name: str
    card_expiration_date: date
    card_cvv: str

    # Validando os campos do modelo
    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('amount must be positive')
        return v

    @validator('payment_method')
    def payment_method_must_be_valid(cls, v):
        if v not in ['debit_card', 'credit_card']:
            raise ValueError('payment_method must be debit_card or credit_card')
        return v

    @validator('card_number')
    def card_number_must_be_valid(cls, v):
        if len(v) != 16 or not v.isdigit():
            raise ValueError('card_number must be a 16-digit number')
        return v

    @validator('card_holder_name')
    def card_holder_name_must_be_valid(cls, v):
        if len(v) == 0 or not all(word.isalpha() for word in v.split()):
            raise ValueError('card_holder_name must be a non-empty string of alphabets')
        return v

    @validator('card_expiration_date')
    def card_expiration_date_must_be_valid(cls, v):
        if v < date.today():
            raise ValueError('card_expiration_date must not be in the past')
        return v

    @validator('card_cvv')
    def card_cvv_must_be_valid(cls, v):
        if len(v) != 3 or not v.isdigit():
            raise ValueError('card_cvv must be a 3-digit number')
        return v


class Payable(BaseModel):
    """
    Modelo de dados para um payable.

    Campos:
        transaction_id (int): O ID da transação associada ao payable.
        status (str): O status do payable.
        payment_date (date): A data de pagamento do payable.
        fee (int): A taxa cobrada na transação.
        amount (int): O valor do payable.
    """
    transaction_id: int
    status: str
    payment_date: date
    fee: int
    amount: int

    # Validando os campos do modelo
    @validator('transaction_id')
    def transaction_id_must_be_valid(cls, v):
        if v <= 0:
            raise ValueError('transaction_id must be positive')
        return v

    @validator('status')
    def status_must_be_valid(cls, v):
        if v not in ['paid', 'waiting_funds']:
            raise ValueError('status must be paid or waiting_funds')
        return v

    @validator('payment_date')
    def payment_date_must_be_valid(cls, v):
        if v < date.today():
            raise ValueError('payment_date must not be in the past')
        return v

    @validator('fee')
    def fee_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('fee must be positive')
        return v

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('amount must be positive')
        return v