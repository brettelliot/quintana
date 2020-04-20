from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from . import app

class DB:

    def __init__(self):
        # Get values from app
        user = app.config['POSTGRES_USER']
        password = app.config['POSTGRES_PASSWORD']
        host = app.config['POSTGRES_HOST']
        database = app.config['POSTGRES_DB']
        port = app.config['POSTGRES_PORT']

        # Build the db URI and keep that as a member
        db_uri = (
            f'postgresql+psycopg2://{user}:{password}@{host}:'
            f'{port}/{database}'
        )

        self._engine = create_engine(db_uri)

        # use session_factory() to get a new Session
        self._session_factory = sessionmaker(bind=self._engine)

        self._base = declarative_base()

    def session_factory(self):
        self._base.metadata.create_all(self._engine)
        return self._session_factory()

    def base(self):
        return self._base

    @contextmanager
    def session_scope(self):
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

_db = DB()

def session_factory():
    return _db.session_factory()

def base():
    return _db.base()

def session_scope():
    return _db.session_scope()
