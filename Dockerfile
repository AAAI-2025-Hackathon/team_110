# Use a minimal Python image to reduce build time
FROM python:3.12.8-slim AS builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libffi-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Second stage - create final image with only necessary files
FROM python:3.12.8-slim
WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app files
COPY . .

# Expose Flask port
EXPOSE 5000

# Run Flask with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
