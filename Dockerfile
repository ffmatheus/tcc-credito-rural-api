FROM python:3.10-slim as base

WORKDIR /app

# Set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.6.1

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock* ./

# Configure Poetry to not use virtualenv
RUN poetry config virtualenvs.create false

# Install dependencies
FROM base as builder
RUN poetry install --no-dev

# Copy application code
COPY src/ ./src/

# Run application
CMD ["uvicorn", "src.presentation.main:app", "--host", "0.0.0.0", "--port", "8000"]