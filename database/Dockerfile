# Choose ubuntu version
FROM mcr.microsoft.com/mssql/server:2022-CU16-ubuntu-22.04

# Create app directory
WORKDIR /usr/src/app

# Copy initialization scripts
COPY . /usr/src/app

# Set environment variables,
ENV SA_PASSWORD=Passw0rd
ENV ACCEPT_EULA=Y

# Expose port
EXPOSE 1433

# Run entry point script
CMD /bin/bash /usr/src/app/entrypoint.sh
