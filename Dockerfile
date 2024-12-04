# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies for SQL Server ODBC driver and mssql-tools
RUN apt-get update && apt-get install -y \
  curl \
  apt-transport-https \
  gnupg && \
  curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
  curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
  apt-get update && ACCEPT_EULA=Y apt-get install -y \
  msodbcsql18 \
  unixodbc-dev \
  mssql-tools18 && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt 

# Expose the port the app runs on
EXPOSE 5000

# Copy and set up the wait script
COPY wait-for-db.sh /app/wait-for-db.sh
RUN chmod +x /app/wait-for-db.sh

# Run the wait script followed by the Flask application
CMD /app/wait-for-db.sh && python run.py

