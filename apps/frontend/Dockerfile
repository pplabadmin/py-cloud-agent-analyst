ARG PYTHON_VERSION=3.14.3
ARG APP_PORT=8080
ARG API_URL=http://localhost:8000
ARG LOG_LEVEL=error

# --- ETAPA 1: BUILDER ---
FROM python:${PYTHON_VERSION}-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y curl unzip && rm -rf /var/lib/apt/lists/*

COPY apps/frontend/ .
RUN pip install --no-cache-dir .

ARG API_URL
ENV API_URL=${API_URL}

RUN reflex init
RUN reflex export --frontend-only --no-zip

# --- ETAPA 2: RUNTIME ---
FROM python:${PYTHON_VERSION}-slim
WORKDIR /app

ARG APP_PORT
ENV PORT=${APP_PORT}

ARG LOG_LEVEL
ENV LOG_LEVEL=${LOG_LEVEL}

RUN apt-get update && apt-get install -y curl unzip && rm -rf /var/lib/apt/lists/*

RUN SITE_PACKAGES=$(python -c "import site; print(site.getsitepackages()[0])") && \
    mkdir -p "$SITE_PACKAGES"

COPY --from=builder /usr/local/lib/python*/site-packages/ /usr/local/lib/temp_packages/

RUN SITE_PACKAGES=$(python -c "import site; print(site.getsitepackages()[0])") && \
    cp -rp /usr/local/lib/temp_packages/. "$SITE_PACKAGES/" && \
    rm -rf /usr/local/lib/temp_packages/

COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

EXPOSE ${APP_PORT}
EXPOSE 8000

ENV HOST=0.0.0.0

CMD ["sh", "-c", "reflex run --env prod --backend-only --address 0.0.0.0 --frontend-port $PORT --loglevel $LOG_LEVEL"]