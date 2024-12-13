from sqlalchemy import create_engine, URL
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = DATABASE_URL = URL.create(
        drivername="postgresql",
        username="postgres",
        password="postgres",
        host="host.docker.internal",
        port="5432",
        database="quiz_db",
    )

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()