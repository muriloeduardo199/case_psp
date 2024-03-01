from faker import Faker

# Cria um objeto Faker
fake = Faker()

# Gera um ID falso
fake_id = fake.unique.random_number(digits=5)

print(fake_id)