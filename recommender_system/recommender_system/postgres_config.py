import os

# Postgres configs
postgres_host, postgres_port = os.getenv("POSTGRES_HOST").split(":")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_db = os.getenv("MLOPS_POSTGRES_DB")