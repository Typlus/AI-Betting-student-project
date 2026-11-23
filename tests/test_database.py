
from database.database import DatabaseManager


def main():

    db = DatabaseManager()

    # Create database tables
    db.initialize_database()

    print("Database initialized successfully!")

    # Register a source
    source_id = db.add_source(
        source_name="Example Sports Statistics",
        source_url="https://example.com"
    )

    # Register a dataset
    dataset_id = db.add_dataset(
        dataset_name="Historical Team Statistics",
        sport="Basketball",
        season="2025-2026"
    )

    # Insert a sample observation
    db.add_observation(
        dataset_id=dataset_id,
        source_id=source_id,
        entity_type="team",
        entity_name="Example Team",
        metric="wins",
        metric_value=45,
        unit="games",
        season="2025-2026",
        event_date="2026-04-15"
    )

    # Retrieve observations
    results = db.get_observations("Example Team")

    print("\n--- STORED OBSERVATIONS ---")

    for result in results:
        print(result)

    print("\n--- DATASETS ---")
    print(db.get_datasets())


if __name__ == "__main__":
    main()
