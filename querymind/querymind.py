import reflex as rx

from .state import State


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("QueryMind: Observabilidad", size="8"),
            rx.card(
                rx.vstack(
                    rx.text("Consulta a BigQuery:", weight="bold"),
                    rx.hstack(
                        rx.input(
                            placeholder="¿Stock de brasil?",
                            on_change=State.set_query,
                            width="100%",
                        ),
                        rx.button(
                            "Consultar",
                            on_click=State.handle_query,
                            loading=State.is_loading,
                            color_scheme="blue",
                        ),
                        width="100%",
                    ),
                ),
                width="100%",
                padding="2em",
            ),
            rx.cond(
                State.show_results,
                rx.vstack(
                    rx.heading("SQL Generado", size="4"),
                    rx.code_block(State.generated_sql, language="sql", width="100%"),
                    rx.heading("Resultado JSON", size="4"),
                    rx.code_block(State.raw_data_json, language="json", width="100%"),
                    width="100%",
                ),
            ),
            rx.cond(
                State.error_message != "",
                rx.callout(
                    State.error_message,
                    icon="triangle_alert",
                    color_scheme="red",
                    width="100%",
                ),
            ),
            width="80%",
            spacing="6",
            padding_y="5em",
        ),
        width="100%",
    )


app = rx.App(theme=rx.theme(appearance="dark", accent_color="blue"))
app.add_page(index, title="QueryMind | Benchmark")
