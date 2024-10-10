from contextlib import contextmanager

import sqlalchemy

from src.settings import database_settings


class Base(sqlalchemy.orm.DeclarativeBase):
    ...


engine = sqlalchemy.create_engine(database_settings.dsn)
print(f"Created engine: {database_settings.dsn}")

Session = sqlalchemy.orm.sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
