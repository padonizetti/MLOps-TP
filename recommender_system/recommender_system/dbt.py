import os
import pandas as pd
import psycopg2

from dagster import AssetExecutionContext, asset, AssetIn, AssetOut, Output
from dagster_dbt import DbtCliResource, get_asset_key_for_model
from dagster_dbt import load_assets_from_dbt_project
from dagster_mlflow import mlflow_tracking

from .constants import dbt_manifest_path, dbt_project_dir

#@dbt_assets(manifest=dbt_manifest_path)
#def db_postgres_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
#    yield from dbt.cli(["build"], context=context).stream()

dbt_assets = load_assets_from_dbt_project(project_dir=str(dbt_project_dir), profiles_dir=str(os.path.expanduser("~/.dbt")))


@asset(compute_kind="python",
       deps=get_asset_key_for_model(dbt_assets, "scores_movies_users")
       )
def training_data(context: AssetExecutionContext)-> Output[pd.DataFrame]:
    
    postgres_host, postgres_port = os.getenv("POSTGRES_HOST").split(":")
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_db = os.getenv("MLOPS_POSTGRES_DB")
    
    conn = psycopg2.connect(
        host=postgres_host,
        port=postgres_port,
        dbname=postgres_db,
        user=postgres_user,
        password=postgres_password
    )
    training_data = pd.read_sql("SELECT * FROM target.scores_movies_users", conn)
    
    return Output(training_data)
