from sqlalchemy import create_engine, URL
from sqlalchemy.orm import declarative_base

DATABASE_URL = DATABASE_URL = URL.create(
        drivername="postgresql",
        username="postgres",
        password="postgres",
        host="host.docker.internal",
        port="5432",
        database="quiz_db",
    )

engine = create_engine(DATABASE_URL)
Base = declarative_base()