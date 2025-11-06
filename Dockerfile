# Dockerfile

# --- Stage 1: Build ---
# Use the same Python version as your local environment
FROM python:3.13-slim as builder

# Set the working directory in the container
WORKDIR /app

# Install system dependencies that might be needed by Python packages
# Added libpq-dev for psycopg2 and zlib1g-dev for image libraries
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev zlib1g-dev

# Copy your production requirements.txt file
COPY requirements.txt .

# --- DEBUG STEP: Print requirements.txt content inside Docker build ---
RUN cat requirements.txt
# --- END DEBUG STEP ---

# Install dependencies directly
RUN pip install --no-cache-dir -r requirements.txt


# --- Stage 2: Run ---
# Use a fresh, clean image with the same Python version
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Create a non-root user for security
RUN useradd --create-home appuser
USER appuser

# Copy the installed dependencies from the builder stage
# This step is no longer copying wheels, but the installed packages from the builder's site-packages
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

# Copy the application code from your local machine into the container
COPY . .

# Set environment variables for Cloud Run
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# The command to run your application in production using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "mysite.wsgi:application"]

# Added a comment to force a rebuild
