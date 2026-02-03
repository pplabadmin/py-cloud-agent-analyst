import glob
import os
import sys

from google.cloud import bigquery

import pandas as pd
from charset_normalizer import from_path

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_NAME = os.getenv("GCP_BQ_DATASET")

if not PROJECT_ID or not DATASET_NAME:
    print("❌ ERROR: GCP_PROJECT_ID o GCP_BQ_DATASET no están definidos en el entorno.")
    print("👉 Ejecuta: source setup_env.sh antes de correr este script.")
    sys.exit(1)

DATASET_ID = f"{PROJECT_ID}.{DATASET_NAME}"
client = bigquery.Client(project=PROJECT_ID)

# Esquemas deterministas
trips_schema = [
    bigquery.SchemaField("Viaje_Id", "INT64"),
    bigquery.SchemaField("Usuario_Id", "INT64"),
    bigquery.SchemaField("Genero", "STRING"),
    bigquery.SchemaField("Año_de_nacimiento", "FLOAT64"),
    bigquery.SchemaField("Inicio_del_viaje", "TIMESTAMP"),
    bigquery.SchemaField("Fin_del_viaje", "TIMESTAMP"),
    bigquery.SchemaField("Origen_Id", "INT64"),
    bigquery.SchemaField("Destino_Id", "INT64"),
]


def ensure_utf8(file_path: str):
    """
    Intenta leer el archivo como UTF-8.
    Solo si falla, detecta el encoding original y lo convierte.
    """
    # 1. Intento de lectura "optimista"
    try:
        with open(file_path, encoding="utf-8") as f:
            f.read()
        # Si llega aquí, el archivo es UTF-8 válido. No hacemos nada.
        print(f"--- [OK] {os.path.basename(file_path)} ya es UTF-8. Saltando...")
        return
    except UnicodeDecodeError:
        # 2. Si falla, el archivo NO es UTF-8. Hay que convertirlo.
        print(
            f"--- [!] {os.path.basename(file_path)} no es UTF-8. Iniciando rescate..."
        )

        # Usamos charset-normalizer para una detección más fina
        results = from_path(file_path).best()

        if results is None:
            raise ValueError(
                f"Inconsistencia crítica: No se pudo determinar el origen de {file_path}"
            ) from None

        detected_encoding = results.encoding
        print(f"--- [!] Detectado {detected_encoding}. Convirtiendo a UTF-8...")

        try:
            # Leemos con el encoding detectado y guardamos como UTF-8
            content = results.string()
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print("--- [EXITO] Archivo convertido correctamente.")
        except Exception as e:
            raise ValueError(
                f"Fallo en consistencia: No se pudo convertir {file_path} ({e})"
            ) from e


def validate_and_process(
    folder_path: str, schema: list[bigquery.SchemaField]
) -> pd.DataFrame:
    all_dfs = []
    expected_cols = [field.name for field in schema]
    files = glob.glob(os.path.join(folder_path, "*.csv"))

    if not files:
        raise FileNotFoundError(f"No se encontraron archivos en {folder_path}")

    for file_path in files:
        # 1. Asegurar UTF-8 antes de leer
        ensure_utf8(file_path)

        # 2. Leer archivo
        df = pd.read_csv(file_path, encoding="utf-8")

        # 3. Normalizar solo variaciones de la 'ñ' por encoding, pero ser estricto con el resto
        df.columns = [
            c.replace("A±o", "Año").replace("Anio", "Año").replace("AÃ±o", "Año")
            for c in df.columns
        ]

        # 4. VALIDACIÓN DE COLUMNAS (FALLA SI FALTA ALGUNA)
        missing_cols = set(expected_cols) - set(df.columns)
        if missing_cols:
            raise ValueError(
                f"CRÍTICO: Al archivo {os.path.basename(file_path)} le faltan columnas: {missing_cols}"
            )

        # 5. VALIDACIÓN DE TIPOS (FECHAS)
        # Sin 'errors=coerce', si una fecha viene mal (ej: texto basura), el script se detiene
        for col in ["Inicio_del_viaje", "Fin_del_viaje"]:
            df[col] = pd.to_datetime(df[col])

        # 6. Ordenar y filtrar solo lo del esquema
        df = df[expected_cols]
        all_dfs.append(df)
        print(f"Archivo verificado y OK: {os.path.basename(file_path)}")

    return pd.concat(all_dfs, ignore_index=True)


def upload_to_bq(df: pd.DataFrame, table_name: str, schema: list[bigquery.SchemaField]):
    # Si llegamos aquí, los datos ya están validados en memoria
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition="WRITE_TRUNCATE",
    )

    print("Iniciando carga final a BigQuery...")
    job = client.load_table_from_dataframe(
        df, f"{DATASET_ID}.{table_name}", job_config=job_config
    )
    job.result()
    print(f"Carga completa. Registros consistentes: {len(df)}")


if __name__ == "__main__":
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        TRIPS_FOLDER = os.path.join(BASE_DIR, "trips_data")

        # El script fallará aquí si algún archivo no cumple el contrato
        final_df = validate_and_process(TRIPS_FOLDER, trips_schema)

        # Solo sube si todos los archivos pasaron la prueba
        upload_to_bq(final_df, "trips", trips_schema)

    except Exception as e:  # pylint: disable=broad-except
        print(f"\n[ERROR DE CONSISTENCIA]: {e}")
        print(
            "La carga ha sido cancelada para proteger la integridad de la base de datos."
        )
        sys.exit(1)
