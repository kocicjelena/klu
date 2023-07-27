import os
import time

from celery import Celery, shared_task, chain
from api import test

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="create_task")
def get_answer(task_type,question):
    dataset = test.get_all_dataset()
    time.sleep(int(task_type) * 1)
    dindex = test.make_index(datatset)
    time.sleep(int(task_type) * 1)
    pick = test.pick(question, dindex, dataset)
    if pick:
        return True

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 1},
             name='dataset:get_all_dataset_task')
def get_all_dataset_task(self):
    data = test.get_all_dataset()
    return data

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 1},
             name='dindex:get_dindex_task')
def get_dindex_task(self, datatset: list):
    dindex = test.make_index(datatset)
    return dindex

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='pick:get_pick_task')
def get_pick_task(self, p: str, dindex: dict, dataset):
    pick = test.pick(p, dindex, dataset)
    return pick





