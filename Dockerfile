# Use an appropriate base image
FROM python:3.9-slim

# Update package lists and install dnsutils (which provides nslookup), curl, and iputils-ping
RUN apt-get update \
    && apt-get install -y dnsutils curl iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all Python files to the image
COPY *.py .
COPY *.sh .
COPY *.txt .
COPY requests.txt .
