###############################################################################################################
#####################################   PUBLIC_DATA_TABLES  ###################################################
create_clients_table="""
            CREATE DATABASE IF NOT EXISTS financas;
            CREATE TABLE IF NOT EXISTS financas.clients (
                id int,
                nome string,
                cpf string,
                tipo_produto string,
                data_nascimento string,
                address string,
                renda_mensal double)
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """

create_employees_table="""
            CREATE DATABASE IF NOT EXISTS financas;
            CREATE TABLE IF NOT EXISTS financas.employees (
                id int,
                nome string,
                cpf string,
                data_inicio string,
                address string,
                salario double,
                area string)
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """

create_operations_table="""
            CREATE DATABASE IF NOT EXISTS financas;
            CREATE TABLE IF NOT EXISTS financas.operations (
                id string,
                cpf string,
                tipo_produto string,
                origem string,
                operacao int,
                valor string,
                online int,
                data string,
                horario string,
                op_timestamp string,
                success int)
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """

drop_financas_database="""
            DROP TABLE IF EXISTS financas.clients;
            DROP TABLE IF EXISTS financas.employees;
            DROP TABLE IF EXISTS financas.operations;
            DROP DATABASE IF EXISTS financas;
        """


