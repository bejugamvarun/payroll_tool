# ---- Build stage ----
FROM python:3.13-slim AS builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# ---- Runtime stage ----
FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy the pre-built virtualenv from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY . .

# Create storage directories
RUN mkdir -p storage/uploads storage/payslips storage/reports

RUN chmod +x entrypoint.sh

# Use venv binaries directly (no uv needed at runtime)
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
