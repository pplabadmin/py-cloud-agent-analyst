import asyncio
import json

import reflex as rx
from dotenv import load_dotenv

from core.tools import bq_executor
from engines.linear.pipeline import get_sql_and_intent

load_dotenv()


class State(rx.State):
    query: str = ""
    is_loading: bool = False
    generated_sql: str = ""
    raw_data_json: str = ""
    error_message: str = ""
    show_results: bool = False

    @rx.event
    async def handle_query(self) -> None:
        if not self.query.strip():
            return

        self.is_loading = True
        self.error_message = ""
        self.show_results = False

        loop = asyncio.get_event_loop()
        try:
            # 1. Generar SQL e Intención
            sql, intent = await loop.run_in_executor(
                None, get_sql_and_intent, self.query
            )
            self.generated_sql = sql

            # 2. Ejecutar contra BigQuery
            res = await loop.run_in_executor(None, bq_executor, sql)

            if res.error:
                self.error_message = res.error
            else:
                output = {
                    "debug": {"intent": intent, "sql": sql},
                    "resultado": {
                        "columnas": res.columns,
                        "filas": len(res.data),
                        "datos": res.data,
                    },
                }
                self.raw_data_json = json.dumps(output, indent=2, ensure_ascii=False)
                self.show_results = True
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
        finally:
            self.is_loading = False
