import asyncio
import logging

import uvicorn

from willow.config import config

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

logging.basicConfig(
    level=logging.INFO if config.environment != "production" else logging.INFO
)


def start():
    logging.info("Starting Willow application...")
    uvicorn.run(
        "willow.utils.starlette:app",
        host="0.0.0.0",
        port=config.port,
        log_level="info" if config.environment != "production" else "warning",
        reload=config.environment == "development",
    )
    # Add your application startup logic here
    # For example, initializing services, loading configurations, etc.
    logging.info("Willow application started successfully.")
