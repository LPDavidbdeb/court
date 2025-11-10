# Dockerfile

# Use the same Python version as your local environment
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    zlib1g-dev \
    # Add any other system dependencies your Court project might need, e.g., gdal-bin, libgdal-dev if using GeoDjango
    && rm -rf /var/lib/apt/lists/*

# Copy your production requirements.txt file
COPY requirements.txt .

# Install dependencies directly
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# NEW: Collect static files for production
# This command will upload static files to GCS if STATICFILES_STORAGE is configured
RUN python manage.py collectstatic --noinput

# Set environment variables for Cloud Run
ENV PORT=8080

# The command to run your application in production using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "mysite.wsgi:application"]
