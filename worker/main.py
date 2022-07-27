from __future__ import annotations

import asyncio
from datetime import timedelta, datetime

from api.models.Schemas.MonitorSchema import MonitorSchema
from worker.Monitor import Monitor
from worker.db import DB
from worker.utils import round_time_to_minutes


FETCH_PERIOD_SEC = 60
CHECK_EVERY_MINUTES = 5
MAX_TASKS = 100


async def worker(name, queue: asyncio.Queue[MonitorSchema]) -> None:
    while True:
        monitor_data = await queue.get()

        dispatch_time = monitor_data.next_check_at.replace(tzinfo=None)
        sleep_time = min(0, (dispatch_time - datetime.utcnow()).total_seconds())

        await asyncio.sleep(sleep_time)

        monitor = Monitor(monitor_data)
        await monitor.check()

        queue.task_done()


async def dispatcher(queue: asyncio.Queue[MonitorSchema]) -> None:
    while True:
        start_time = round_time_to_minutes(datetime.utcnow(), base_minutes=CHECK_EVERY_MINUTES)
        monitors = DB.fetch_monitors(FETCH_PERIOD_SEC)
        print(f'fetched {len(monitors)} monitors')

        await asyncio.gather(*[queue.put(monitor) for monitor in monitors])

        await queue.join()
        DB.commit()

        next_iteration_at = start_time + timedelta(minutes=float(CHECK_EVERY_MINUTES))

        delay = max(next_iteration_at.timestamp() - datetime.utcnow().timestamp(), 0)
        await asyncio.sleep(delay)


async def run():
    tasks = []
    task_dispatcher = None
    queue: asyncio.Queue[MonitorSchema] = asyncio.Queue()

    for i in range(MAX_TASKS):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    task_dispatcher = asyncio.create_task(dispatcher(queue))
    await task_dispatcher


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
