import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "mssql+pyodbc://sa:Passw0rd@sqlserver:1433/recipe_db?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&ConnectionTimeout=60",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
