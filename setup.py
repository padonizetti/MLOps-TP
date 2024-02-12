from setuptools import find_packages, setup
import os
DAGSTER_VERSION=os.getenv('DAGSTER_VERSION', '1.6.4')
DAGSTER_LIBS_VERSION=os.getenv('DAGSTER_LIBS_VERSION', '0.22.4')
MLFLOW_VERSION=os.getenv('MLFLOW_VERSION', '2.10.0')

setup(
    name="recommender_system",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        f"dagster=={DAGSTER_VERSION}",
        f"dagit=={DAGSTER_VERSION}",
        "dagster-dbt",
        "dbt-postgres",
        f"dagster-mlflow=={DAGSTER_LIBS_VERSION}",
        f"mlflow=={MLFLOW_VERSION}",
        "tensorflow==2.14.0",
    ],
    extras_require={
        "dev": ["dagster-webserver", "pytest", "jupyter"], "tests": ["mypy", "pylint", "pytest"]
    },
)