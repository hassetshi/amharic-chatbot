# Use official Python runtime as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port (Cloud Run will set PORT env variable)
EXPOSE 8080

# Set environment variable for Streamlit
ENV PORT=8080

# Create .streamlit directory and config
RUN mkdir -p ~/.streamlit/

# Run streamlit
CMD streamlit run app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.serverAddress="0.0.0.0" \
    --browser.gatherUsageStats=false
