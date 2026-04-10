# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variable for OpenAI API (placeholder, should be passed at runtime)
# ENV HF_TOKEN=your_token_here

# Command to run the FastAPI app as a server (Mandatory for OpenEnv Reset check)
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
