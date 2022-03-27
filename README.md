# DATA MASTER LAKE CASE

## História (Simulação descrita nesse case)


O banco Santander antes de migrar para um sistema de armazenamento distribuido, guardava seus dados em bancos SQL. Em determinado momento, meados de 2013, os engenheiros de dados do banco, ao notar como o volume de informação chegando só crescia, chegaram ao consenso de que seria preciso armazenar esses dados de forma distribuida.
Uma nova tecnologia da Apache havia sido criada poucos anos atrás e as grandes empresas todas estavam migrando para esse tipo de arquitetura de dados. Era o famoso HADOOP.
Após muito trabalho do time de especialistas, um cluster HADOOP On Premisse foi criado.

## Desenho de arquitetura




## Pipeline "mysql_ingestion_pipeline"
Essa pipeline em resumo consiste em 2 vertentes diferentes.

#### Vertente 1:
  - Criação de dados aleatórios para entidades cliente, funcionário e operações
  - Inserção dos dados em um banco MySQL (tabelas clients, employees, operations)
  - Ingestão dos dados no lake utilizando o kafka e kafka connect
  - Criação de tabelas Hive par colocar dados das tabela citadas
  - Execução de jobs pyspark para inserir os dados ingestados nas 3 tabelas Hive criadas

#### Vertente 2:
  - Download de dados estruturados do marcado de ações (Ibovespa)
  - Inserção dos dados em um banco MySQL ()
  - Ingestão dos dados no lake utilizando o kafka e kafka connect
  - Criação de tabelas Hive par colocar dados das tabela citadas
  - Execução de jobs pyspark para inserir os dados ingestados nas tabelas Hive criadas

### Passo a passo para executar pipeline com sucesso e ver resultados:
  - Execute o script ./start.sh e espere até todos os containers subirem
  - Crie as conexões do Kafka connect no Control-Center (localhost:9021)
  - Execute a pipeline "mysql_ingestion_pipeline.
  - Consulte tabelas criadas no serviço "mysql".
  - Consulte tópicos gerados no Kafka e listados no Control Center (aba topics)
  - Consulte diretórios criados no HDFS através do HUE (localhost:32762)
  - Consulte tabelas criadas no HIVE, através do HUE (localhost:32762)

##### Conectores do Kafka para esse pipeline:
  Ingestão de dados fakes do santander
    MysqlSourceConnectors:
      - /mnt/airflow/dags/scripts/kafka_connect_files/mysqlSource_santander_data.properties
    HDFSSinkConnectors:
      - /mnt/airflow/dags/scripts/kafka_connect_files/hdfsSink_santander_clients_migration.properties
      - /mnt/airflow/dags/scripts/kafka_connect_files/hdfsSink_santander_employees_migration.properties
      - /mnt/airflow/dags/scripts/kafka_connect_files/hdfsSink_santander_operations_migration.properties
  
  Ingestão de dados reais do Mercado de ações (Ibovespa) usando biblioteca "yahooquery"
    MysqlSourceConnectors:
      - /mnt/airflow/dags/scripts/kafka_connect_files/mysqlSource_stock_market_data.properties
    HDFSSinkConnectors:
      - /mnt/airflow/dags/scripts/kafka_connect_files/hdfsSink_stockmarket_b3_migration.properties


## Pipeline "mongo_ingestion_pipeline"

#### Vertente 1 (Hipotetica aquisição do nubank):
  - Criação de dados aleatórios para entidades cliente, funcionário e operações.
  - Inserção dos dados em um banco Mongo (coleções clients, employees, operations) chamado "nubank_data".
  - Criação de tabelas Hive par colocar dados das coleções citadas.
  - Execução de jobs pyspark para ler as coleções do mongo citadas acima, processar e inserir os dados nas respectivas tabelas.

#### Vertente 2:
  - Criação de dados aleatórios para entidades facebook e public_survey.
  - Inserção dos dados em um banco Mongo (coleções facebook e public_survey) chamado santander_marketing.
  - Ingestão dos dados no lake utilizando o kafka e kafka connect
  - Criação de tabelas Hive par colocar dados das coleções citadas
  - Execução de jobs pyspark para inserir os dados ingestados nas tabelas Hive criadas.


### Passo a passo para executar pipeline com sucesso e ver resultados:
  - Execute o script ./start.sh e espere até todos os containers subirem
  - Execute a pipeline "mongo_ingestion_pipeline.
  - Consulte coleções criadas no serviço mongo.
  - Consulte tópicos gerados no Kafka e listados no Control Center (aba topics).
  - Consulte diretórios criados no HDFS através do HUE (localhost:32762)
  - Consulte tabelas criadas no HIVE, através do HUE (localhost:32762)


## Pipeline "streamming_operations_pipeline"
    - python caixa_agencia_streaming.py --freq 1000 & python atm_streaming.py --freq 1000 & python mobile_streaming.py --freq 1000 & python maquininhas_streaming.py --freq 1000 & python internet_banking_streaming.py --freq 1000

##### Conectores do Kafka para esse pipeline:
  Ingestão de dados fakes de operações do banco:
    HDFSSinkConnectors:
      - /mnt/airflow/dags/scripts/kafka_connect_files/hdfsSink_santander_clients_migration.properties
      - /mnt/airflow/dags/scripts/kafka_connect_files/hdfsSink_santander_employees_migration.properties
      - /mnt/airflow/dags/scripts/kafka_connect_files/hdfsSink_santander_operations_migration.properties
  
  Ingestão de dados reais do Mercado de ações (Ibovespa) usando biblioteca "yahooquery"
    MysqlSourceConnectors:
      - /mnt/airflow/dags/scripts/kafka_connect_files/mysqlSource_stock_market_data.properties
    HDFSSinkConnectors:
      - /mnt/airflow/dags/scripts/kafka_connect_files/hdfsSink_stockmarket_b3_migration.properties


### Passo a passo para executar pipeline com sucesso e ver resultados:
  - Execute o script ./start.sh e espere até todos os containers subirem
  - Crie as conexões do Kafka connect no Control-Center (localhost:9021)
  - Execute o script ./run_operations.sh, dentro do serviço "producers"
  - Execute a pipeline "streamming_operations_pipeline.
  - Consulte tópicos gerados no Kafka e listados no Control Center (aba topics)
  - Consulte diretórios criados no HDFS através do HUE (localhost:32762)
  - Consulte tabelas criadas no HIVE, através do HUE (localhost:32762)

## Pipeline "process_finances"