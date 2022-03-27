from .nubank_fake_data import create_nubank_operation, create_nubank_client, create_nubank_employee
from .public_fake_data import create_facebook_survey_fake, create_public_survey_fake
from .utils_dbs import populate_mongo_db

def populate_nubank_mongodb_operations(host, port, db, collection, num_rows):
    populate_mongo_db(host, port, db, collection, num_rows, create_nubank_operation)

def populate_nubank_mongodb_clients(host, port, db, collection, num_rows):
    populate_mongo_db(host, port, db, collection, num_rows, create_nubank_client)

def populate_nubank_mongodb_employees(host, port, db, collection, num_rows):
    populate_mongo_db(host, port, db, collection, num_rows, create_nubank_employee)

def populate_public_mongodb_facebook_survey(host, port, db, collection, num_rows):
    populate_mongo_db(host, port, db, collection, num_rows, create_facebook_survey_fake)

def populate_public_mongodb_survey(host, port, db, collection, num_rows):
    populate_mongo_db(host, port, db, collection, num_rows, create_public_survey_fake)
