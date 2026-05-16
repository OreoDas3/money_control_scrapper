import logging
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas


def load_to_snowflake(df, config):
    snowflake_config = config["snowflake"]
    load_config = config["snowflake_load"]

    conn = None
    cursor = None

    try:
        logging.info("Connecting to Snowflake")

        conn = snowflake.connector.connect(
            account=snowflake_config["account"],
            user=snowflake_config["user"],
            password=snowflake_config["password"],
            role=snowflake_config["role"],
            warehouse=snowflake_config["warehouse"],
            database=snowflake_config["database"],
            schema=snowflake_config["schema"]
        )

        cursor = conn.cursor()

        table_name = load_config["table_name"]

        if load_config["recreate_table"]:
            logging.info(f"Recreating table: {table_name}")

            cursor.execute(f"""
                CREATE OR REPLACE TABLE {table_name} (
                    ID NUMBER AUTOINCREMENT,
                    TITLE STRING,
                    AUTHOR STRING,
                    PUBLICATION_DATE STRING,
                    ARTICLE_URL STRING,
                    CONTENT STRING
                )
            """)

        logging.info("Loading dataframe into Snowflake")

        success, nchunks, nrows, _ = write_pandas(
            conn=conn,
            df=df,
            table_name=table_name,
            auto_create_table=False
        )

        if success:
            logging.info(
                f"Successfully loaded {nrows} rows into Snowflake "
                f"using {nchunks} chunk(s)"
            )
        else:
            logging.error("write_pandas returned unsuccessful status")

    except snowflake.connector.Error as e:
        logging.error(f"Snowflake error: {e}")

    except Exception as e:
        logging.error(f"Unexpected loader error: {e}")

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

        logging.info("Snowflake connection closed")