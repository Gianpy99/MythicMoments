
import sqlite3
from datetime import datetime
import random
import os

DB_FILE = "daily_fantasy_events.db"

class DailyFantasyDB:
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file
        self.conn = None
        self._connect()
        self._create_tables()

    def _connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
        except sqlite3.Error as e:
            print(f"[ERROR] Unable to connect to database: {e}")
            raise

    def _create_tables(self):
        try:
            c = self.conn.cursor()
            # Giorni
            c.execute("""
            CREATE TABLE IF NOT EXISTS days (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month INTEGER NOT NULL,
                day INTEGER NOT NULL,
                UNIQUE(month, day)
            )
            """)
            # Eventi
            c.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day_id INTEGER NOT NULL,
                universe TEXT NOT NULL,       -- "Tolkien", "HarryPotter", "Matrix"
                year TEXT,
                fact TEXT,
                quote TEXT,
                position INTEGER DEFAULT 1,
                FOREIGN KEY(day_id) REFERENCES days(id)
            )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Unable to create tables: {e}")
            raise

    def populate_days(self):
        """Popola tutti i giorni dell’anno (senza bisestile)"""
        try:
            c = self.conn.cursor()
            for month in range(1, 13):
                if month in [1,3,5,7,8,10,12]:
                    days_in_month = 31
                elif month in [4,6,9,11]:
                    days_in_month = 30
                else:
                    days_in_month = 28
                for day in range(1, days_in_month + 1):
                    c.execute("INSERT OR IGNORE INTO days (month, day) VALUES (?, ?)", (month, day))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Unable to populate days: {e}")
            raise

    def get_day_id(self, month, day):
        """Restituisce l'id del giorno"""
        c = self.conn.cursor()
        c.execute("SELECT id FROM days WHERE month=? AND day=?", (month, day))
        res = c.fetchone()
        if res:
            return res[0]
        return None

    def add_event(self, month, day, universe, year, fact, quote="", position=1):
        """Aggiunge un evento al DB"""
        day_id = self.get_day_id(month, day)
        if not day_id:
            print(f"[WARNING] Day {month}/{day} not found in DB. Populating days...")
            self.populate_days()
            day_id = self.get_day_id(month, day)
        try:
            c = self.conn.cursor()
            c.execute("""
                INSERT INTO events (day_id, universe, year, fact, quote, position)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (day_id, universe, year, fact, quote, position))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Unable to add event: {e}")
            raise

    def get_events_for_day(self, month=None, day=None):
        """Recupera tutti gli eventi di un giorno (default: oggi)"""
        if not month or not day:
            today = datetime.now()
            month = today.month
            day = today.day
        day_id = self.get_day_id(month, day)
        if not day_id:
            return {}

        c = self.conn.cursor()
        c.execute("""
            SELECT universe, year, fact, quote, position
            FROM events
            WHERE day_id=?
            ORDER BY universe, position
        """, (day_id,))
        rows = c.fetchall()
        events_by_universe = {}
        for universe, year, fact, quote, position in rows:
            if universe not in events_by_universe:
                events_by_universe[universe] = []
            events_by_universe[universe].append({
                "year": year,
                "fact": fact,
                "quote": quote,
                "position": position
            })
        return events_by_universe

    def get_random_event_of_day(self, month=None, day=None):
        """Restituisce un evento casuale per universo del giorno"""
        all_events = self.get_events_for_day(month, day)
        random_events = {}
        for universe, events in all_events.items():
            random_events[universe] = random.choice(events)
        return random_events

    def close(self):
        if self.conn:
            self.conn.close()


# ------------------ ESEMPIO USO ------------------
if __name__ == "__main__":
    db = DailyFantasyDB()

    # Popola giorni (solo una volta)
    db.populate_days()

    # Aggiungi eventi di esempio
    sample_events = [
        (12, 12, "Tolkien", "3018 TA", "Frodo leaves the Shire"),
        (12, 13, "Tolkien", "3018 TA", "Council of Elrond begins"),
        (12, 14, "HarryPotter", "1993", "Triwizard Tournament begins"),
        (12, 15, "Matrix", "1999", "Neo confronts Agent Smith"),
    ]
    for month, day, universe, year, fact in sample_events:
        db.add_event(month, day, universe, year, fact)

    # Estrai un evento casuale del giorno
    events_today = db.get_random_event_of_day()
    for universe, event in events_today.items():
        print(f"{universe} ({event['year']}): {event['fact']}")
        if event['quote']:
            print(f"Quote: {event['quote']}")
        print()

    db.close()


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
