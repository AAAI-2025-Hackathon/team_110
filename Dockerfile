# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#RUN python ./utils/db_setup.py

# Copy app files
COPY . .

# Expose Flask port
EXPOSE 5000

# Run Flask with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]