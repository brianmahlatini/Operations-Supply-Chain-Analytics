# Operations & Supply Chain Analytics

Business-facing BI solution for inventory, fulfilment, supplier performance, lead-time reliability, operational cost control, stockout detection, and service-level improvement.

This project turns an operations analytics brief into a portfolio-ready reporting product with:

- PostgreSQL data model and reusable SQL metric views
- Synthetic supply-chain data generator for realistic demo scale
- FastAPI backend exposing KPI, supplier, inventory, and bottleneck endpoints
- React dashboard for management-facing operational monitoring
- Power BI-ready DAX measures and SQL references
- Docker Compose environment for one-command local execution

## Tech Stack

| Layer | Technologies |
| --- | --- |
| Business Intelligence | Power BI, DAX, Power Query |
| Backend API | Python, FastAPI, SQLAlchemy, Pydantic |
| Frontend | React, Vite, Recharts, Lucide React, CSS |
| Database | PostgreSQL, SQL views |
| Analytics | Python, pandas, supplier and inventory analytics |
| DevOps | Docker, Docker Compose |
| Documentation | Markdown, SQL and DAX references |

## Architecture

```text
Power BI / React Dashboard
          |
          v
FastAPI Operations API
          |
          v
PostgreSQL warehouse tables and SQL views
          |
          v
Python synthetic data and reproducible analysis assets
```

## Project Structure

```text
.
|-- analysis/
|   |-- generate_synthetic_data.py
|   `-- operations_analysis.py
|-- backend/
|   |-- app/
|   |   |-- api/routes.py
|   |   |-- core/config.py
|   |   |-- core/database.py
|   |   |-- models/schemas.py
|   |   |-- services/analytics.py
|   |   `-- main.py
|   |-- Dockerfile
|   `-- requirements.txt
|-- data/
|   |-- inventory_movements.csv
|   |-- order_lines.csv
|   |-- purchase_orders.csv
|   `-- shipments.csv
|-- database/
|   |-- 01_schema.sql
|   |-- 02_seed.sql
|   |-- 03_views.sql
|   `-- 04_generated_fact_seed.sql
|-- docs/
|   `-- sql_queries.sql
|-- frontend/
|   |-- src/
|   |   |-- components/KpiCard.jsx
|   |   |-- lib/api.js
|   |   |-- main.jsx
|   |   `-- styles.css
|   |-- Dockerfile
|   |-- index.html
|   |-- package.json
|   `-- vite.config.js
|-- powerbi/
|   `-- dax_measures.md
|-- docker-compose.yml
`-- README.md
```

## Business Questions Answered

- Which suppliers are causing late deliveries and longer lead times?
- Which products and regions show stockout or backorder risk?
- How well are orders being fulfilled against requested units?
- Which inventory items are turning slowly or falling below reorder point?
- What is the combined operational cost from freight, transport, and holding cost?
- Where should management focus process improvement efforts first?

## Metrics

| Metric | Definition |
| --- | --- |
| Service Level | Fulfilled units divided by ordered units |
| Stockout Rate | Order lines flagged as stockout divided by total order lines |
| On-Time Delivery Rate | Purchase orders delivered on or before expected date |
| Average Lead Time | Days between purchase order date and actual delivery date |
| Inventory Turnover | Issued units divided by average inventory units |
| Days Below Reorder Point | Count of inventory periods where closing stock is below reorder point |
| Operational Cost | Freight cost plus transport cost plus inventory holding cost |

## Run With Docker

Requirements:

- Docker Desktop
- Docker Compose

Start the full stack:

```bash
docker compose up --build
```

Services:

- React dashboard: `http://localhost:5175`
- FastAPI docs: `http://localhost:8002/docs`
- API health check: `http://localhost:8002/api/health`
- PostgreSQL: `localhost:5434`

Database credentials for local development:

- Database: `operations_analytics`
- User: `analytics`
- Password: `analytics_password`

Stop the stack:

```bash
docker compose down
```

Reset the database seed data:

```bash
docker compose down -v
docker compose up --build
```

## API Endpoints

| Endpoint | Purpose |
| --- | --- |
| `GET /api/health` | Service health check |
| `GET /api/kpis` | Service level, stockout rate, lead time, cost, delays |
| `GET /api/suppliers` | Supplier lead time, on-time delivery, delay and quality metrics |
| `GET /api/product-region` | Drill-down by product, supplier, and region |
| `GET /api/inventory-turnover` | Inventory turnover and reorder-point risk |
| `GET /api/recommendations` | Bottleneck and process-improvement recommendations |

## React Dashboard

The dashboard includes:

- KPI cards for service level, on-time delivery, stockouts, lead time, operational cost, and delays
- Supplier reliability bar chart
- Product and region bottleneck drill-down table
- Supplier lead-time panel
- Process improvement recommendations

## SQL Analytics

Metric logic is centralized in SQL views so Power BI, the API, and ad hoc analysis use consistent definitions.

Key views:

- `vw_operational_kpis`
- `vw_supplier_performance`
- `vw_inventory_turnover`
- `vw_order_fulfillment`
- `vw_product_region_performance`

Reference SQL is available in `docs/sql_queries.sql`.

## Generate Synthetic Data

Use the generator when you want a different data volume or a fresh scenario.

```bash
python analysis/generate_synthetic_data.py --months 12 --orders 1000 --seed 99
```

Generated outputs:

- `data/purchase_orders.csv`
- `data/order_lines.csv`
- `data/shipments.csv`
- `data/inventory_movements.csv`
- `database/04_generated_fact_seed.sql`

PostgreSQL loads files in the `database/` folder in alphabetical order on first container initialization.

## Power BI Build Guide

1. Open Power BI Desktop.
2. Select Get Data > PostgreSQL database.
3. Connect to `localhost:5434`.
4. Database: `operations_analytics`.
5. Import the base tables and SQL views.
6. Add the DAX measures in `powerbi/dax_measures.md`.
7. Build these report pages:
   - Executive Overview
   - Inventory Turnover & Stockout Risk
   - Supplier Lead Time & On-Time Delivery
   - Product, Supplier & Region Drill-Down
   - Operational Cost and Delay Bottlenecks

Suggested visuals:

- KPI cards for service level, stockouts, delays, lead time, and cost
- Bar chart for supplier on-time delivery
- Matrix visual for product by region fulfilment
- Table visual for SKUs below reorder point
- Slicers for product category, supplier, region, and month

## Python Reproducible Analysis

Run after starting Docker:

```bash
python analysis/operations_analysis.py
```

Install local Python dependencies if running outside Docker:

```bash
pip install pandas sqlalchemy psycopg[binary]
```

## Portfolio Narrative

Recommended CV wording:

Built a Dockerized Operations & Supply Chain Analytics platform using PostgreSQL, FastAPI, React, Python, SQL, DAX, and Power BI. Developed reusable SQL views for inventory turnover, stockout rate, order fulfilment, supplier lead time, on-time delivery, operational cost, and service-level reporting. Delivered an executive dashboard and drill-down analysis by product, supplier, and region to identify bottlenecks and recommend process improvements.

Evidence to include:

- Screenshot of React dashboard
- Screenshot of Power BI supplier and inventory pages
- Link to `/docs` API page
- SQL views used for reusable metric definitions
- DAX measure file
- Python synthetic data generator output

## Senior-Level Design Notes

- Metric definitions live in PostgreSQL views to keep Power BI and API outputs aligned.
- The backend keeps routing, database access, schemas, and analytics services separated.
- Pydantic response models provide stable API contracts.
- Docker Compose includes a database health check so the API waits for PostgreSQL readiness.
- The generated data includes realistic operational variance: late suppliers, backorders, stockouts, lead-time pressure, quality issues, and holding costs.
- The dashboard supports management review while keeping drill-down paths by product, supplier, and region.

## Next Enhancements

- Add dbt models for lineage, tests, and production-grade transformation documentation.
- Add pytest coverage for API contracts and SQL view outputs.
- Add Power BI `.pbix` report once the visual layout is finalized.
- Add forecast-based reorder point recommendations.
- Add supplier scorecards with contractual SLA thresholds.
