import os

import reflex as rx

config = rx.Config(
    app_name="querymind",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    api_url=os.getenv("API_URL", "http://localhost:8000"),
    cors_allowed_origins=[
        "https://querymind.pepelab.dev",
        "http://localhost:3000",
        "http://localhost:8000",
    ],
)
