import contextlib
import logging
from time import time

from aiohttp import ClientSession
from starlette.applications import Starlette

from willow.config import config
from willow.tasks import register_tasks
from willow.utils.logging import send_heartbeat
from willow.utils.signal import SignalApi

logger = logging.getLogger(__name__)


class Environment:
    http: ClientSession

    @contextlib.asynccontextmanager
    async def enter(self, _app: Starlette):
        st = time()
        logger.debug("Entering environment context")
        self.http = ClientSession()
        self.signal = SignalApi(
            number=config.signal.number,
            api_key=config.signal.api_key,
            base_url=config.signal.base_url,
            session=self.http,
        )

        await register_tasks(self.signal)

        logger.debug(f"Environment setup in {time() - st:.02}s")
        await send_heartbeat(
            "willow up!",
            client=self.signal,
        )

        yield

        await send_heartbeat(
            "willow down!",
            client=self.signal,
        )

        await self.http.close()


env = Environment()
