import json
from unittest.mock import patch

from worker import get_all_dataset_task


def test_home(test_app):
    response = test_app.get("/")
    assert response.status_code == 200


def test_task():
    assert get_all_dataset_task.run()

