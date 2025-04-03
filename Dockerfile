# Use the official Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download necessary NLTK datasets
RUN python -m nltk.downloader averaged_perceptron_tagger punkt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the ports on which the app will run
EXPOSE 8001 8002

# Default command (will be overridden by docker-compose)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]
