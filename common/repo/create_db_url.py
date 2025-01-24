from sqlalchemy import URL
from pydantic_settings import BaseSettings


def create_db_url_from_settings(settings: BaseSettings) -> URL:
    return URL.create(
        drivername=settings.drivername,
        username=settings.username,
        password=settings.password,
        host=settings.host,
        port=settings.port,
        database=settings.database,
    )