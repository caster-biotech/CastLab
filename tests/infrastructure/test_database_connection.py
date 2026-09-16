from sqlalchemy import text

def test_sqlite_pragmas(engine, session):
    with engine.connect() as conn:
        journal_mode = conn.execute(text("PRAGMA journal_mode;")).scalar()
        assert journal_mode in ("wal", "memory")

        foreign_keys = conn.execute(text("PRAGMA foreign_keys;")).scalar()
        assert foreign_keys == 1
