<!-- @format -->

## Desafio Técnico - Backend Pleno

O desafio consiste na construção de um PSP (Payment Service Provider) simplificado. Em sua essência um PSP tem duas funções muito importantes:

Iremos trabalhar com duas entidades principais:

-   `transactions`: que representam as informações da compra, dados do cartão, valor, etc
-   `payables`: que representam os recebíveis que pagaremos ao cliente

## **Requisitos obrigatórios**

Você deve criar um serviço com os seguintes requisitos:

1. O serviço deve processar transações, recebendo as seguintes informações:
    - Valor da transação
    - Descrição da transação.
    - Método de pagamento (`debit_card` ou `credit_card`)
    - Número do cartão
    - Nome do portador do cartão
    - Data de validade do cartão
    - Código de verificação do cartão (CVV)
2. O serviço deve retornar uma lista das transações já criadas
3. Você deve se preocupar com a segurança de dados sensíveis.
4. O serviço deve criar os recebíveis do cliente (`payables`), com as seguintes regras:
    - Se a transação for feita com um cartão de débito:
        - O payable deve ser criado com status = `paid` (indicando que o cliente já recebeu esse valor)
        - O payable deve ser criado com a data de pagamento (payment_date) = data da criação da transação (D+0).
    - Se a transação for feita com um cartão de crédito:
        - O payable deve ser criado com status = `waiting_funds` (indicando que o cliente vai receber esse dinheiro no futuro)
        - O payable deve ser criado com a data de pagamento (payment_date) = data da criação da transação + 30 dias (D+30).
5. No momento de criação dos payables também deve ser descontado a taxa de processamento (que chamamos de `fee`) do cliente. Ex: se a taxa for 5% e o cliente processar uma transação de R$100.00, ele só receberá R$95.00. Considere as seguintes taxas:
    - 3% para transações feitas com um cartão de débito
    - 5% para transações feitas com um cartão de crédito
6. O serviço deve prover um meio de consulta para que o cliente visualize seu saldo com as seguintes informações:
    - Saldo `available` (disponível): tudo que o cliente já recebeu (payables `paid`)
    - Saldo `waiting_funds` (a receber): tudo que o cliente tem a receber (payables `waiting_funds`)

> Nota: neste desafio, você não precisa se preocupar com parcelamento.

## Restrições

1. O serviço deve ser escrito em Javascript (É permitido o uso de Typescript) ou em Python
2. O serviço deve armazenar informações em um banco de dados. Você pode escolher o banco que achar melhor.
3. O projeto deve conter testes unitários.

## Entrega

1. O desafio deve ser enviado para a pessoa que estiver em contato com você, no formato de `.zip` ou um link para um repositório do Github
2. Iremos te avaliar pela arquitetura do serviço, qualidade do código, entendimento das regras de negócio, capricho com o desafio.
