import logging

from willow.config import config
from willow.utils.signal import SignalApi


async def send_heartbeat(message, client: SignalApi, level=logging.INFO):
    logging.log(level, f"Heartbeat: {message}")
    await client.send_message(recipient=config.signal.log_group, message=message)
