FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (layer caching)
COPY pyproject.toml ./
# Copy source and data
COPY sage/ sage/
COPY data/ data/
COPY CLAUDE.md ./
RUN pip install --no-cache-dir .
ENV PYTHONPATH=/app
EXPOSE 8501

# Railway sets PORT; pass it to Streamlit at runtime
CMD streamlit run sage/app.py --server.port ${PORT:-8501} --server.address 0.0.0.0