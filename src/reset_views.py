from sqlalchemy import create_engine, text
from src.config import DATABASE_URL


def main():
    engine = create_engine(DATABASE_URL)

    queries = [
        "DROP VIEW IF EXISTS avg_temp_por_dispositivo CASCADE;",
        "DROP VIEW IF EXISTS leituras_por_hora CASCADE;",
        "DROP VIEW IF EXISTS temp_max_min_por_dia CASCADE;"
    ]

    with engine.connect() as conn:
        for query in queries:
            conn.execute(text(query))
        conn.commit()

    print("Views removidas com sucesso!")


if __name__ == "__main__":
    main()