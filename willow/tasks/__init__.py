from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from willow.config import config
from willow.tasks.receive_messages import receive_messages
from willow.utils.signal import SignalApi


async def register_tasks(client: SignalApi):
    scheduler = AsyncIOScheduler(timezone=config.timezone)
    scheduler.add_job(
        func=receive_messages,
        args=[client],
        trigger="interval",
        seconds=1,
        max_instances=1,
        next_run_time=datetime.now(),
    )

    scheduler.start()
