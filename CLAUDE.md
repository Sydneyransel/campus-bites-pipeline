# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A local data pipeline that loads Campus Bites order data (CSV) into a PostgreSQL database running in Docker, for analysis purposes.

## Setup & Commands

**Start the database:**
```bash
docker compose up -d
```

**Load data into the database:**
```bash
python load_data.py
```

**Connect to the database (psql):**
```bash
docker exec -it campus_bites_db psql -U postgres -d campus_bites
```

**Tear down (preserves data volume):**
```bash
docker compose down
```

**Tear down and delete all data:**
```bash
docker compose down -v
```

## Database

- Host: `localhost`, Port: `5433`
- Database: `campus_bites`, User/Password: `postgres/postgres`
- Single table: `orders`

**Schema:**
| Column | Type |
|---|---|
| order_id | INTEGER PRIMARY KEY |
| order_date | DATE NOT NULL |
| order_time | TIME NOT NULL |
| customer_segment | VARCHAR(50) NOT NULL |
| order_value | NUMERIC(8,2) NOT NULL |
| cuisine_type | VARCHAR(50) NOT NULL |
| delivery_time_mins | INTEGER NOT NULL |
| promo_code_used | VARCHAR(3) |
| is_reorder | VARCHAR(3) |

## Architecture

Data flow: `data/campus_bites_orders.csv` → `load_data.py` (psycopg2 batch insert) → PostgreSQL 16 (Docker)

`load_data.py` drops and recreates the `orders` table on each run, then batch-inserts all rows, converting empty strings to NULL for nullable columns (`promo_code_used`, `is_reorder`).

## Dependencies

- Docker Desktop (required for the database)
- Python with `psycopg2` installed (in `.venv/`)
