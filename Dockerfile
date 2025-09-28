# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install extra dependencies
RUN pip install pyyaml

# Copy the rest of the code
COPY . .

# Default command: run main.py
CMD ["python", "main.py"]
