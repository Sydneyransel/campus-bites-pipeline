import csv
import psycopg2

# Connection parameters for the local PostgreSQL database running in Docker
DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "campus_bites",
    "user": "postgres",
    "password": "postgres",
}

# Path to the CSV file containing order data
CSV_PATH = "data/campus_bites_orders.csv"

# SQL statement to create the orders table if it doesn't already exist
CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    order_id           INTEGER PRIMARY KEY,
    order_date         DATE NOT NULL,
    order_time         TIME NOT NULL,
    customer_segment   VARCHAR(50) NOT NULL,
    order_value        NUMERIC(8, 2) NOT NULL,
    cuisine_type       VARCHAR(50) NOT NULL,
    delivery_time_mins INTEGER NOT NULL,
    promo_code_used    VARCHAR(3),
    is_reorder         VARCHAR(3)
);
"""

# SQL statement to insert a single row into the orders table
INSERT_ROW = """
INSERT INTO orders (
    order_id, order_date, order_time, customer_segment,
    order_value, cuisine_type, delivery_time_mins,
    promo_code_used, is_reorder
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
"""


def load():
    # Open a connection to the database
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn:
            with conn.cursor() as cur:
                # Create the orders table if it doesn't exist
                cur.execute(CREATE_TABLE)

                # Read all rows from the CSV into a list of tuples
                with open(CSV_PATH, newline="") as f:
                    reader = csv.DictReader(f)
                    rows = [
                        (
                            row["order_id"],
                            row["order_date"],
                            row["order_time"],
                            row["customer_segment"],
                            row["order_value"],
                            row["cuisine_type"],
                            row["delivery_time_mins"],
                            row["promo_code_used"] or None,  # Convert empty string to NULL
                            row["is_reorder"] or None,       # Convert empty string to NULL
                        )
                        for row in reader
                    ]

                # Insert all rows in a single batch operation
                cur.executemany(INSERT_ROW, rows)
                print(f"Loaded {len(rows)} rows into orders table.")
    finally:
        # Always close the connection, even if an error occurred
        conn.close()


if __name__ == "__main__":
    load()
