from clickhouse_connect.driver import Client

def init_clickhouse_schema(client: Client):
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS events (
            user_id Int32,
            post_id Int32,
            type LowCardinality(String),
            timestamp DateTime
        ) ENGINE = MergeTree()
        ORDER BY (post_id, timestamp)
    '''
    client.command(create_table_query)