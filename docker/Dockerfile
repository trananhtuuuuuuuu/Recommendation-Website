FROM python:3.13-alpine

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

RUN apk add --no-cache gcc musl-dev python3-dev linux-headers

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY . .

# Expose the API port 
EXPOSE 8386

# Command to run the FastAPI application with uvicorn
CMD ["python", "run.py"]

