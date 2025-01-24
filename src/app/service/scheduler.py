from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from app.db import sync_engine

jobstores = {'default': SQLAlchemyJobStore(engine=sync_engine)}
executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},
    'processpool': ProcessPoolExecutor(max_workers=5),
}
job_defaults = {'coalesce': True, 'max_instances': 3}
scheduler = AsyncIOScheduler(
    jobstores=jobstores,
    job_defaults=job_defaults,
    timezone=utc,
)
