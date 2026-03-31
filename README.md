# Campus Bites Pipeline

Local Postgres database for analyzing Campus Bites order data.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Setup

```bash
# 1. Clone the repo
git clone <repo-url>
cd campus-bites-pipeline

# 2. Start the database
docker compose up -d

# 3. Verify it's running
docker compose ps
```

The database is ready when the container status shows `healthy` or `running`. On first startup, Postgres will automatically create the `orders` table and load the CSV — this takes a few seconds.

## Connect

| Setting  | Value          |
|----------|----------------|
| Host     | localhost      |
| Port     | 5433           |
| Database | campus_bites   |
| User     | postgres       |
| Password | postgres       |

**psql (command line)**
```bash
docker exec -it campus_bites_db psql -U postgres -d campus_bites

# Or via TCP (e.g. if local PostgreSQL is also running on 5432)
psql "postgresql://postgres:postgres@localhost:5433/campus_bites"
```

**Any SQL client** (DBeaver, TablePlus, pgAdmin, etc.) — use the connection settings above.

## Schema

```sql
CREATE TABLE orders (
    order_id           INTEGER PRIMARY KEY,
    order_date         DATE,
    order_time         TIME,
    customer_segment   VARCHAR(50),  -- e.g. 'Grad Student', 'Off-Campus'
    order_value        NUMERIC(8,2),
    cuisine_type       VARCHAR(50),  -- e.g. 'Asian', 'Indian', 'Breakfast'
    delivery_time_mins INTEGER,
    promo_code_used    VARCHAR(3),   -- 'Yes' or 'No'
    is_reorder         VARCHAR(3)    -- 'Yes' or 'No'
);
```

## Common Queries

```sql
-- Row count
SELECT COUNT(*) FROM orders;

-- Revenue by cuisine
SELECT cuisine_type, ROUND(SUM(order_value), 2) AS total_revenue
FROM orders
GROUP BY cuisine_type
ORDER BY total_revenue DESC;

-- Average delivery time by customer segment
SELECT customer_segment, ROUND(AVG(delivery_time_mins), 1) AS avg_delivery_mins
FROM orders
GROUP BY customer_segment
ORDER BY avg_delivery_mins;

-- Promo code usage rate
SELECT promo_code_used, COUNT(*) AS orders, ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
FROM orders
GROUP BY promo_code_used;
```

## Tear Down

```bash
# Stop the container (data is preserved)
docker compose down

# Stop and delete all data (full reset)
docker compose down -v
```

To reload the CSV from scratch after a full reset, just run `docker compose up -d` again.
