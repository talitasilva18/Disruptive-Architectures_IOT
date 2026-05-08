from sqlalchemy import create_engine, text
from src.config import DATABASE_URL


def main():
    engine = create_engine(DATABASE_URL)

    queries = [
        """
        CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
        SELECT
            location_type,
            ROUND(AVG(temperature)::numeric, 2) AS avg_temp
        FROM temperature_readings
        WHERE location_type IS NOT NULL
        GROUP BY location_type
        ORDER BY location_type;
        """,

        """
        CREATE OR REPLACE VIEW leituras_por_hora AS
        SELECT
            EXTRACT(HOUR FROM noted_date) AS hora,
            COUNT(*) AS contagem
        FROM temperature_readings
        WHERE noted_date IS NOT NULL
        GROUP BY EXTRACT(HOUR FROM noted_date)
        ORDER BY hora;
        """,

        """
        CREATE OR REPLACE VIEW temp_max_min_por_dia AS
        SELECT
            DATE(noted_date) AS data,
            ROUND(MAX(temperature)::numeric, 2) AS temp_max,
            ROUND(MIN(temperature)::numeric, 2) AS temp_min
        FROM temperature_readings
        WHERE noted_date IS NOT NULL
        GROUP BY DATE(noted_date)
        ORDER BY data;
        """
    ]

    with engine.connect() as conn:
        for query in queries:
            conn.execute(text(query))
        conn.commit()

    print("Views SQL criadas com sucesso!")


if __name__ == "__main__":
    main()