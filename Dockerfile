# =============================================================================
# McDill University Advancement Analytics & CASE Intelligence Portal
# Dockerfile - Production Containerization for Streamlit
# =============================================================================

# BASE IMAGE: Use Debian slim variant of Python 3.11 to minimize container image
# footprint, reduce attack surface, and ensure fast cold starts on cloud hosts.
FROM python:3.11-slim

# PYTHON ENVIRONMENT CONFIGURATION:
# - PYTHONDONTWRITEBYTECODE=1: Prevents Python from writing .pyc bytecode to disk
# - PYTHONUNBUFFERED=1: Ensures stdout and stderr are sent straight to logs without buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# STREAMLIT RUNTIME DEFAULTS:
# Pre-configure server flags for containerized, non-interactive production hosting.
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Set application working directory inside container
WORKDIR /app

# SYSTEM DEPENDENCIES:
# Install curl for container orchestration health checks, then clean apt cache to save space.
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# DOCKER LAYER CACHING STRATEGY:
# Copy requirements.txt separately and install Python dependencies before copying source code.
# This prevents re-installing packages (streamlit, pandas, numpy, plotly) on every code edit.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# APPLICATION CODE:
# Copy remaining source code, CSV data extracts, and Streamlit theme configurations.
COPY . .

# EXPOSE DEFAULT STREAMLIT PORT (Documentation only; runtime binds dynamically)
EXPOSE 8501

# HEALTHCHECK:
# Render and Docker orchestration probe Streamlit's internal health endpoint.
HEALTHCHECK CMD curl --fail http://localhost:${PORT:-8501}/_stcore/health || exit 1

# DYNAMIC PORT BINDING:
# Render and cloud container platforms inject an arbitrary $PORT environment variable at runtime.
# Using a shell wrapper ensures ${PORT:-8501} falls back gracefully to 8501 for local Docker runs.
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0"]
