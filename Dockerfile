# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables (customize as needed)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files to the container
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
