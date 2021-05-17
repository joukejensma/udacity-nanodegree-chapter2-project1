import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    This method loads the staging tables from AWS S3 into Redshift staging tables for a given cursor cur and connection conn.
    Returns: None
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    This method inserts the requisited data from the staging tables into the analysis tables for a given cursor cur and connection conn.
    Returns: None
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Worker function that connects to the AWS Redshift cluster with settings taken from dwh.cfg.
    After that, the staging tables are loaded and the analysis tables are filled.
    Finally, the connection is closed.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()