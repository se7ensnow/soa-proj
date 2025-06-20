import pytest
from uuid import uuid4
from datetime import datetime
from stats_service_app import crud

class MockClient:
    def __init__(self, rows):
        self._rows = rows

    def query(self, _):
        class Result:
            def __init__(self, rows):
                self.result_rows = rows
        return Result(self._rows)

def test_get_post_stats():
    mock = MockClient([[10, 5, 3]])
    result = crud.get_post_stats(mock, uuid4())
    assert result == {"views": 10, "likes": 5, "comments": 3}

def test_get_post_metric_by_day():
    mock = MockClient([[datetime(2025, 6, 18).date(), 42]])
    result = crud.get_post_metric_by_day(mock, uuid4(), 'view')
    assert result == [{"date": datetime(2025, 6, 18).date(), "count": 42}]

def test_get_top_posts_by():
    mock = MockClient([["post-id", 99]])
    result = crud.get_top_posts_by(mock, "like")
    assert result == [{"id": "post-id", "count": 99}]

def test_invalid_metric_raises():
    with pytest.raises(ValueError):
        crud.get_post_metric_by_day(MockClient([]), uuid4(), "invalid")