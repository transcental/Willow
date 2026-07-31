from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine

from willow.config import config

DB = PostgresEngine(config={"dsn": config.database_url.encoded_string()})

APP_REGISTRY = AppRegistry(apps=["willow.piccolo_app"])
