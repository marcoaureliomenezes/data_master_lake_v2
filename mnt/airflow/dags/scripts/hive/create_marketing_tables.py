###############################################################################################################
#####################################   PUBLIC_DATA_TABLES  ###################################################
create_facebook_table="""
            CREATE DATABASE IF NOT EXISTS marketing;
            CREATE TABLE IF NOT EXISTS marketing.facebook (
                name string,
                age int,
                banco string,
                bank_fan_pages array<string>)
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """

create_public_survey_table="""
            CREATE DATABASE IF NOT EXISTS marketing;
            CREATE TABLE IF NOT EXISTS marketing.public_survey (
                name string,
                address string,
                age int,
                banco string,
                nota_geral string,
                servico_mais_usado string)
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """

drop_marketing_database="""
            DROP TABLE IF EXISTS marketing.facebook;
            DROP TABLE IF EXISTS marketing.twitter;
            DROP TABLE IF EXISTS marketing.public_survey;
            DROP DATABASE IF EXISTS marketing;
        """


create_twitter_table= """
            CREATE DATABASE IF NOT EXISTS marketing;
            CREATE TABLE IF NOT EXISTS marketing.twitter(
                id int,
                userId int,
                geolocation string,
                retweet_count string,
                text string,
                in_reply_to_user_id int)
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """
        