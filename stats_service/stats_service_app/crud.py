from clickhouse_connect.driver import Client
from datetime import datetime

def insert_event(client: Client, user_id: int, post_id: int, event_type: str, timestamp: datetime):
    print("INSERTING EVENT", user_id, post_id, event_type, timestamp)
    data = [[user_id, post_id, event_type, timestamp]]
    client.insert(
        table='events',
        data=data,
        column_names=['user_id', 'post_id', 'type', 'timestamp']
    )

def get_post_stats(client: Client, post_id: int) -> dict:
    query = f"""
        SELECT
            countIf(type = 'view') AS views,
            countIf(type = 'like') AS likes,
            countIf(type = 'comment') AS comments
        FROM events
        WHERE post_id = '{post_id}'
    """
    result = client.query(query)
    row = result.result_rows[0]
    return {
        'views': row[0],
        'likes': row[1],
        'comments': row[2]
    }

def get_post_metric_by_day(client: Client, post_id: int, metric: str) -> list[dict]:
    if metric not in ['view', 'like', 'comment']:
        raise ValueError(f'Invalid metric {metric}')

    query = f"""
        SELECT toDate(timestamp) AS day, count(*) AS count
        FROM events
        WHERE post_id = '{post_id}' AND type = '{metric}'
        GROUP BY day
        ORDER BY day
    """
    result = client.query(query)
    return [{"date": row[0], "count": row[1]} for row in result.result_rows]

def get_top_posts_by(client: Client, metric: str) -> list[dict]:
    if metric not in ['view', 'like', 'comment']:
        raise ValueError(f'Invalid metric {metric}')

    query = f"""
        SELECT post_id, count(*) AS count
        FROM events
        WHERE type = '{metric}'
        GROUP BY post_id
        ORDER BY count DESC
        LIMIT 10
    """

    result = client.query(query)
    return [{"id": row[0], "count": row[1]} for row in result.result_rows]

def get_top_users_by(client: Client, metric: str) -> list[dict]:
    if metric not in ['view', 'like', 'comment']:
        raise ValueError(f'Invalid metric {metric}')

    query = f"""
        SELECT user_id, count(*) AS count
        FROM events
        WHERE type = '{metric}'
        GROUP BY user_id
        ORDER BY count DESC
        LIMIT 10
    """

    result = client.query(query)
    return [{"id": row[0], "count": row[1]} for row in result.result_rows]