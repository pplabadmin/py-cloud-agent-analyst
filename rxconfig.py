import os

import reflex as rx

config = rx.Config(
    app_name="querymind",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    api_url=os.getenv("API_URL", "http://localhost:8080"),
    backend_port=int(os.getenv("PORT", "8080")),
    frontend_port=int(os.getenv("PORT", "8080")),
    transport="websocket",
)
