KLU


sysctl vm.overcommit_memory=1

$ docker-compose up -d --build


http://localhost:8004

monitor app (Flower): http://localhost:5556 

Note:




- Websocket is used for chat as suitable for real time apps, 
- FastAPI improves transaction per second along many other features, 
- Celery is replacing background task of fast API (request/response flow is not blocked).

Benchmark using flower is getting dataset in o.012s if dataset is array of two object.

The list for obligatory concept improvement:
- Parallelism in handling celery task (chat for million of users)
- Data structure and concept can be more optimised, still using FastAPI:
	- using alchemy integration (along with session) and making index for dataset in db
	- Inject dependencies into API endpoints *
    - Taking care of questions in row, probably **	
    - integration of Jupyter notebook, multiple server processes etc.
    - Add workers
    - Monitor task queues by celery needs to be more detailed: The client ->FastAPI app->message broker-> Celery workers (saving and updating task status)

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

 