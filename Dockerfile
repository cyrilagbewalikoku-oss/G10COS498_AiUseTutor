FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (layer caching)
COPY pyproject.toml ./
# Copy source and the canonical data tree (scenarios, rubrics, seed users, etc.)
COPY sage/ sage/
COPY data/ data/
COPY CLAUDE.md ./
RUN pip install --no-cache-dir .
ENV PYTHONPATH=/app
EXPOSE 8501

# Railway persistence:
#   1. Set the SAGE_DATA_DIR env var in the Railway dashboard, e.g. /mnt/sage-data
#   2. Mount a Railway volume at that same path
# On first boot, sage.session_store.seed_if_empty() copies the image's /app/data
# tree into the volume so scenarios/rubrics/seed profiles are available.
# If SAGE_DATA_DIR is unset, the app falls back to /app/data (ephemeral).

# Railway sets PORT; pass it to Streamlit at runtime
CMD streamlit run sage/app.py --server.port ${PORT:-8501} --server.address 0.0.0.0
