KLU


sysctl vm.overcommit_memory=1

$ docker-compose up -d --build


http://localhost:8004
monitor app (Flower): http://localhost:5556 

remark:

- Working with DataSet on huggingface:
python -c "from datasets import load_dataset; 
print(load_dataset('squad', split='train')[0])"

The measurement of simple chat is out of the concept of fast and reliable enterprise app: this is
FastAPI app using celery and redis. 
- Websocket is used for chat as suitable for real time apps, 
- FastAPI improves transaction per second along many other features, 
- Celery is replacing background task of fast API (request/response flow is not blocked).

Benchmark using flower is getting dataset in o.012s if dataset is array of two object.

Beside implementing concept of Async request handling and data fetching, background task which are replaced by celery and redis, caching, CORS current concept improvements are endless:
- Parallelism in handling celery task (chat for million of users), celery task handling some some common functionalities for chat
- Data structure and concept would be more optimised, still using FastAPI:
	- Beside using out of the box alchemy integration (along with session) and making real case and making index for dataset in db, and not currently implemented indexing in dict (which is generating in every call of the app and celery tasks)
	Inject dependencies into API endpoints *
    - Taking care of questions in row, probably **	
    - Additionaly FastAPI provides blueprint for all numbered and plus integration of Jupyter notebook, multiple server processes etc.
    - Add workers
    - Monitor task queues by celery needs to be more detailed: The client ->FastAPI app->message broker-> Celery workers (saving and updating task status)
    - Flower is used for benchmark but it is overall useful for monitoring.

- Making authentication and authorisation for users 
- Optimise CORS for separate read and write

* @app.get("/datasets/")
async def read_datasets(database: dict = Depends(get_database)):
return {"database": database}
** @router.get("/")
def get_conversations(
params: PaginationParams = Depends(),
session: Session = Depends(get_session)
) -> List[Conv]:
with session.begin():
query = (f"SELECT * FROM Conv ORDER BY id OFFSET {params.skip}"
f" ROWS FETCH NEXT {params.limit} ROWS ONLY")
result = session.execute(text(query))
answer = [Conv(**dict(row)) for row in result.fetchall()]
return answer



REFERENCE:
https://fastapi.tiangolo.com/
https://docs.celeryq.dev/en/stable/userguide/workers.html

 