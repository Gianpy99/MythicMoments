import sqlite3

class DailyFantasyDB:
    def __init__(self, db_path="daily_fantasy.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL,
            universe TEXT NOT NULL,
            year TEXT,
            fact TEXT,
            quote TEXT,
            event_index INTEGER DEFAULT 1,
            UNIQUE(month, day, universe, event_index)
        )
        """)
        self.conn.commit()

    def add_event(self, month, day, universe, year=None, fact=None, quote=None, event_index=1):
        try:
            self.conn.execute("""
            INSERT INTO daily_events (month, day, universe, year, fact, quote, event_index)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (month, day, universe, year, fact, quote, event_index))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Event already exists for {month}/{day} {universe} index {event_index}")

    def get_events_for_day(self, month, day):
        cur = self.conn.cursor()
        cur.execute("SELECT universe, year, fact, quote FROM daily_events WHERE month=? AND day=?", (month, day))
        rows = cur.fetchall()
        events = {}
        for universe, year, fact, quote in rows:
            events.setdefault(universe, []).append({'year': year, 'fact': fact, 'quote': quote})
        return events
