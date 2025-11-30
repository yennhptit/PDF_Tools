# Base image
FROM python:3.11-slim

# Cài Ghostscript và build tools
RUN apt-get update && apt-get install -y ghostscript build-essential && apt-get clean

# Thư mục làm việc
WORKDIR /app

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Expose port
EXPOSE 5000

# Start Flask app
CMD ["python", "app.py"]
