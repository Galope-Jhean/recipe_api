#!/bin/bash

echo "Starting initialization script..."

# Wait for SQL Server to be ready
until /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -C -Q "SELECT 1" > /dev/null 2>&1; do
    echo "Waiting for SQL Server to be ready..."
    sleep 5
done

echo "SQL Server is ready. Running database creation script..."

# Execute the SQL script
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -C -d master -i /usr/src/app/create-database.sql

echo "Database creation script executed."
