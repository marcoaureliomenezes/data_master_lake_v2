from .utils_random_data import gen_address, gen_distinct, gen_name
from .utils_data import bancos
from random import randint

def create_facebook_survey_fake():
    return {
        "name": gen_name(),
        "age": randint(18, 50),
        "address": gen_address(),
        "bank_fan_pages": list(set([gen_distinct(bancos) for i in range(randint(1, 4))])),
        "banco": gen_distinct(["santander", "caixa", "nubank"]),
        "amigos":[{"name": gen_name(), "banco": gen_distinct(bancos)}for i in range(randint(2, 5))]
    }


def create_public_survey_fake():
    return {
        "name": gen_name(),
        "age": randint(18, 50),
        "address": gen_address(),
        "banco": gen_distinct(["santander", "caixa", "nubank"]),
        "nota_geral": randint(1,5),
        "servico_mais_usado": gen_distinct(["ATM", "caixa Agencia", "mobile", "internet_banking"])
    }

if __name__ == '__main__':
    print(create_facebook_survey_fake())
    print(create_public_survey_fake())