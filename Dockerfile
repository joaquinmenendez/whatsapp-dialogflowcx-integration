# Base image with Python installed
FROM python:3.9-slim
# Working directory
WORKDIR /app
# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
# Copy app code
COPY . /app
# Run the Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]