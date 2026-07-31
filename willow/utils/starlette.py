import logging

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from willow.config import config
from willow.env import env

logger = logging.getLogger(__name__)


async def health(req: Request):
    signal_healthy = await env.signal.api_test()
    db_healthy = True  # TODO: Implement database health check

    return JSONResponse(
        {
            "healthy": signal_healthy and db_healthy,
            "signal": signal_healthy,
            "database": db_healthy,
        }
    )


app = Starlette(
    debug=True if config.environment != "production" else False,
    routes=[
        Route(path="/health", endpoint=health, methods=["GET"]),
    ],
    lifespan=env.enter,
)
