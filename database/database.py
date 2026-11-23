
import sqlite3
from pathlib import Path
from datetime import datetime, timezone


# Database location
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "sports_res.db"


class DatabaseManager:

    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = Path(database_path)

        # Create the data directory if it doesn't exist
        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def connect(self):
        """Create and return a database connection."""

        connection = sqlite3.connect(self.database_path)

        # Return rows as dictionaries-like objects
        connection.row_factory = sqlite3.Row

        # Enable foreign key constraints
        connection.execute("PRAGMA foreign_keys = ON")

        return connection

    def initialize_database(self):
        """Create the database tables."""

        with self.connect() as connection:

            connection.executescript("""
                CREATE TABLE IF NOT EXISTS datasets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dataset_name TEXT NOT NULL,
                    sport TEXT,
                    season TEXT,
                    last_updated TEXT,
                    latest_event_date TEXT,
                    record_count INTEGER DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_name TEXT NOT NULL,
                    source_url TEXT NOT NULL,
                    retrieval_date TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS observations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dataset_id INTEGER,
                    source_id INTEGER,
                    entity_type TEXT NOT NULL,
                    entity_name TEXT NOT NULL,
                    metric TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    unit TEXT,
                    season TEXT,
                    event_date TEXT,

                    FOREIGN KEY (dataset_id)
                        REFERENCES datasets(id),

                    FOREIGN KEY (source_id)
                        REFERENCES sources(id)
                );

                CREATE TABLE IF NOT EXISTS research_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    research_topic TEXT NOT NULL,
                    execution_date TEXT NOT NULL,
                    status TEXT,
                    summary TEXT
                );
            """)

    def add_source(self, source_name, source_url):
        """Save a research source."""

        with self.connect() as connection:

            cursor = connection.execute("""
                INSERT INTO sources (
                    source_name,
                    source_url,
                    retrieval_date
                )
                VALUES (?, ?, ?)
            """, (
                source_name,
                source_url,
                datetime.now(timezone.utc).isoformat()
            ))

            return cursor.lastrowid

    def add_dataset(self, dataset_name, sport, season):
        """Register a collected dataset."""

        with self.connect() as connection:

            cursor = connection.execute("""
                INSERT INTO datasets (
                    dataset_name,
                    sport,
                    season,
                    last_updated
                )
                VALUES (?, ?, ?, ?)
            """, (
                dataset_name,
                sport,
                season,
                datetime.now(timezone.utc).isoformat()
            ))

            return cursor.lastrowid

    def add_observation(
        self,
        dataset_id,
        source_id,
        entity_type,
        entity_name,
        metric,
        metric_value,
        unit=None,
        season=None,
        event_date=None
    ):
        """Store a historical statistical observation."""

        with self.connect() as connection:

            connection.execute("""
                INSERT INTO observations (
                    dataset_id,
                    source_id,
                    entity_type,
                    entity_name,
                    metric,
                    metric_value,
                    unit,
                    season,
                    event_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                dataset_id,
                source_id,
                entity_type,
                entity_name,
                metric,
                metric_value,
                unit,
                season,
                event_date
            ))

            connection.execute("""
                UPDATE datasets
                SET record_count = record_count + 1,
                    last_updated = ?
                WHERE id = ?
            """, (
                datetime.now(timezone.utc).isoformat(),
                dataset_id
            ))

    def get_observations(self, entity_name):
        """Retrieve stored statistics for a team or player."""

        with self.connect() as connection:

            cursor = connection.execute("""
                SELECT
                    observations.*,
                    sources.source_name,
                    sources.source_url
                FROM observations
                LEFT JOIN sources
                    ON observations.source_id = sources.id
                WHERE observations.entity_name = ?
                ORDER BY observations.event_date
            """, (entity_name,))

            return [dict(row) for row in cursor.fetchall()]

    def get_datasets(self):
        """Retrieve registered datasets."""

        with self.connect() as connection:

            cursor = connection.execute("""
                SELECT * FROM datasets
                ORDER BY last_updated DESC
            """)

            return [dict(row) for row in cursor.fetchall()]
