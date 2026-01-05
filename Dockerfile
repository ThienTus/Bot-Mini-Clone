FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy scraper code
COPY scraper/ /app/scraper/

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/scraper/requirements.txt

# Run the daily job once and exit
CMD ["python", "scraper/main.py"]
