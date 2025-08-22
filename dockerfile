# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (for some libraries like pandas, TA-Lib, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code into container
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command to run the bot
CMD ["python", "src/main.py"]
