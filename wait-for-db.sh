#!/bin/bash

SERVER="sqlserver"  # SQL Server container hostname
USER="SA"
PASSWORD="Passw0rd"
MAX_RETRIES=30  # Maximum retries before failing

echo "Waiting for SQL Server to be ready..."

# Loop to check SQL Server connectivity
for i in $(seq 1 $MAX_RETRIES); do
  # Attempt to connect to SQL Server
  /opt/mssql-tools18/bin/sqlcmd -S $SERVER -U $USER -P $PASSWORD -C -Q "SELECT 1" > /dev/null 2>&1
  
  # If connection is successful, break out of the loop
  if [ $? -eq 0 ]; then
    echo "SQL Server is ready!"
    exit 0
  fi

  echo "Attempt $i/$MAX_RETRIES: SQL Server not ready, checking again..."
  sleep 5
done

echo "SQL Server failed to start within the maximum retry attempts."
exit 1

