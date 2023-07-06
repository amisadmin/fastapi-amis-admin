# Scheduled tasks

`FastAPI-Amis-Admin` is based on `APScheduler` to provide a simple and powerful timed task system for the system in the form of application plug-ins.

## Project Introduction

`FastAPI-Scheduler` is a simple scheduled task management `FastAPI` extension library based on `APScheduler`.

- Project address: [FastAPI-Scheduler](https://github.com/amisadmin/fastapi_scheduler)

## Install

```bash
pip install fastapi-scheduler
```

## Simple example

```python
from fastapi import FastAPI
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from datetime import date
from fastapi_scheduler import SchedulerAdmin

# Create `FastAPI` application
app = FastAPI()

# Create `AdminSite` instance
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))

# Create an instance of the scheduled task scheduler `SchedulerAdmin`
scheduler = SchedulerAdmin.bind(site)


# Add scheduled tasks, refer to the official documentation: https://apscheduler.readthedocs.io/en/master/
# use when you want to run the job at fixed intervals of time
@scheduler.scheduled_job('interval', seconds=60)
def interval_task_test():
    print('interval task is run...')


# use when you want to run the job periodically at certain time(s) of day
@scheduler.scheduled_job('cron', hour=3, minute=30)
def cron_task_test():
    print('cron task is run...')


# use when you want to run the job just once at a certain point of time
@scheduler.scheduled_job('date', run_date=date(2022, 11, 11))
def date_task_test():
    print('date task is run...')


# Mount the background management system
site.mount_app(app)


@app.on_event("startup")
async def startup():
    # Start the scheduled task scheduler
    scheduler.start()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
```

## Interface preview

- Open `http://127.0.0.1:8000/admin/` in your browser:

![SchedulerAdmin](https://s2.loli.net/2022/05/10/QEtCLsWi1389BKH.png)

## Dependent projects

- [FastAPI-Amis-Admin](https://docs.amis.work/)

- [APScheduler](https://apscheduler.readthedocs.io/en/master/)