import pandas as pd
from sqlalchemy import create_engine
from src.config import DATABASE_URL


def main():
    arquivo_csv = "data/IOT-temp.csv"

    df = pd.read_csv(arquivo_csv)

    df.columns = [
        col.strip()
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        for col in df.columns
    ]

    if "id" in df.columns:
        df = df.rename(columns={"id": "device_id"})

    if "room_id_id_habitacion" in df.columns:
        df = df.rename(columns={"room_id_id_habitacion": "room_id"})

    if "temp" in df.columns:
        df = df.rename(columns={"temp": "temperature"})

    if "out_in" in df.columns:
        df = df.rename(columns={"out_in": "location_type"})

    if "noted_date" in df.columns:
        df["noted_date"] = pd.to_datetime(
            df["noted_date"],
            errors="coerce",
            dayfirst=True
        )

    print("Colunas tratadas:")
    print(df.columns.tolist())
    print(df.head())

    engine = create_engine(DATABASE_URL)

    df.to_sql(
        "temperature_readings",
        engine,
        if_exists="replace",
        index=False
    )

    print("Dados inseridos com sucesso no PostgreSQL!")
    print(f"Total de registros inseridos: {len(df)}")


if __name__ == "__main__":
    main()