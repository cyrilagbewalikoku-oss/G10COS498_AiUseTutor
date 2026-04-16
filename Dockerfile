FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (layer caching)
COPY pyproject.toml ./
RUN pip install --no-cache-dir .

# Copy source and data
COPY sage/ sage/
COPY data/ data/
COPY CLAUDE.md ./

# Default to CLI agent (matches Procfile)
CMD ["python", "-m", "sage.agent"]