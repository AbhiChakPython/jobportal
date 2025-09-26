# -----------------------------
# Base image
# -----------------------------
FROM python:3.13-slim

# -----------------------------
# Environment variables
# -----------------------------
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# -----------------------------
# Set working directory
# -----------------------------
WORKDIR /app

# -----------------------------
# Install system dependencies
# -----------------------------
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Copy requirements and install
# -----------------------------
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Copy project files
# -----------------------------
COPY . /app/

# -----------------------------
# Expose port
# -----------------------------
EXPOSE 8000

# -----------------------------
# Default command
# -----------------------------
CMD ["gunicorn", "jobportal.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
