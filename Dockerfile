# Use official Python runtime as base image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory in the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from the current directory to the container
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "Home.py"]
