from .utils_dbs import populate_mysql_db
from sqlalchemy import create_engine
from .santander_fake_data import create_santander_operation, create_santander_client_sql, \
                                create_santander_employee, get_historic_stock_data

def populate_santander_operations_mysql_table(conn_dict, db_name, table_name, num_rows):
    schema_operation = {"cpf": "VARCHAR(64)", "tipo_produto": "VARCHAR(256)", "origem": "VARCHAR(256)", 
    "operacao": "VARCHAR(64)", "valor": "DOUBLE", "online": "INT", "data": "VARCHAR(64)","horario": "VARCHAR(64)", 
    "op_timestamp": "VARCHAR(256)", "success": "INT"}
    populate_mysql_db(conn_dict, db_name, table_name, schema=schema_operation, method_data_generator=create_santander_operation, num_rows=num_rows)

def populate_santander_clients_mysql_table(conn_dict, db_name, table_name, num_rows):
    schema_client = {
        "nome": "VARCHAR(256)", "cpf": "VARCHAR(32)", "tipo_produto": "VARCHAR(256)", "data_nascimento": "VARCHAR(256)", "address": "VARCHAR(256)", "renda_mensal": "DOUBLE"
    }
    populate_mysql_db(conn_dict, db_name, table_name, schema=schema_client, method_data_generator=create_santander_client_sql, num_rows=num_rows)


def populate_santander_employees_mysql_table(conn_dict, db_name, table_name, num_rows):
    schema_employee = {
        "nome": "VARCHAR(256)", "cpf": "VARCHAR(32)", "data_inicio": "VARCHAR(256)", "address": "VARCHAR(256)",
        "salario": "DOUBLE", "area": "VARCHAR(256)"}
    
    populate_mysql_db(conn_dict, db_name, table_name, schema=schema_employee, method_data_generator=create_santander_employee, num_rows=num_rows)

def populate_stock_market_table(conn_dict, table_name, tickers=["ECOR3.SA", "BBDC3.SA", "ENBR3.SA", "BBDC4.SA"]):
    user, password, service = [conn_dict.get(key) for key in ["user", "password", "host"]]
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{service}/stock_market')
    for ticker in tickers:
        dataframe = get_historic_stock_data(ticker)
        dataframe.to_sql(table_name, con = engine,if_exists='append')
    return

if __name__ == '__main__':

    conn_dict = {
    "user": "root", 
    "password":"root", 
    "host":'172.20.0.6', 
    "port": 3306, 
    "db": "mysql"}
    populate_stock_market_table(conn_dict, "bovespa")