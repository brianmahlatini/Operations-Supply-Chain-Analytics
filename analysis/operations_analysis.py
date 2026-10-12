import os

import pandas as pd
from sqlalchemy import create_engine


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://analytics:analytics_password@localhost:5434/operations_analytics",
)


def main():
    engine = create_engine(DATABASE_URL)
    queries = {
        "Operational KPIs": "SELECT * FROM vw_operational_kpis",
        "Supplier Performance": "SELECT * FROM vw_supplier_performance ORDER BY on_time_delivery_rate ASC",
        "Product Region Bottlenecks": """
            SELECT *
            FROM vw_product_region_performance
            ORDER BY stockout_rate DESC, days_below_reorder_point DESC
            LIMIT 10
        """,
    }

    for title, query in queries.items():
        print(f"\n{title}")
        print(pd.read_sql(query, engine).to_string(index=False))


if __name__ == "__main__":
    main()
