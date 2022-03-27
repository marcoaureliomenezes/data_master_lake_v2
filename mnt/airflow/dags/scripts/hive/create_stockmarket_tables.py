###############################################################################################################
#####################################   PUBLIC_DATA_TABLES  ###################################################
create_ibovespa_table="""
            CREATE DATABASE IF NOT EXISTS stock_market;
            CREATE TABLE IF NOT EXISTS stock_market.ibovespa (
                index int,
                symbol string,
                datet int,
                high double,
                open double,
                close double,
                volume int,
                low double,
                adjclose double,
                dividends double)
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """

drop_stock_market_database="""
            DROP TABLE IF EXISTS stock_market.ibovespa;
            DROP DATABASE IF EXISTS stock_market;
        """

