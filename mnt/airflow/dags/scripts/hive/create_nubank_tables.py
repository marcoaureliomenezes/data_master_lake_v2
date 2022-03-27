###############################################################################################################
#####################################   PUBLIC_DATA_TABLES  ###################################################
create_clients_table="""
            CREATE DATABASE IF NOT EXISTS nubank_data;
            CREATE TABLE IF NOT EXISTS nubank_data.clients (
                nome string,
                cpf string,
                data_nascimento string,
                limite float,
                renda_mensal double,
                saldo double,
                tipo_produto string)
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """

create_employees_table="""
            CREATE DATABASE IF NOT EXISTS nubank_data;
            CREATE TABLE IF NOT EXISTS nubank_data.employees (
                nome string,
                cpf string,
                data_inicio string,
                salario float,
                area string)
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """

create_operations_table="""
            CREATE DATABASE IF NOT EXISTS nubank_data;
            CREATE TABLE IF NOT EXISTS nubank_data.operations (
                cpf string,
                data string,
                horario string,
                op_timestamp int,
                valor double,
                tipo_produto array<string>,
                success int)
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """

drop_nubank_database="""
            DROP TABLE IF EXISTS nubank_data.clients;
            DROP TABLE IF EXISTS nubank_data.employees;
            DROP TABLE IF EXISTS nubank_data.operations;
            DROP DATABASE IF EXISTS nubank_data;
        """


