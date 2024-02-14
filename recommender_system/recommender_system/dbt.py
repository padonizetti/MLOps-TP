import os
import pandas as pd
import psycopg2

from dagster import AssetExecutionContext, asset, AssetIn, AssetOut, Output
from dagster_dbt import DbtCliResource, dbt_assets, get_asset_key_for_model
from dagster_mlflow import mlflow_tracking

from .constants import dbt_manifest_path

postgres_host, postgres_port = os.getenv("POSTGRES_HOST").split(":")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_db = os.getenv("MLOPS_POSTGRES_DB")

@dbt_assets(manifest=dbt_manifest_path)
def db_postgres_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


#def fetch_data_from_db(table_name: str) -> pd.DataFrame:
#    conn = psycopg2.connect(
#        host=postgres_host,
#        port=postgres_port,
#        dbname=postgres_db,
#        user=postgres_user,
#        password=postgres_password
#    )
#    df = pd.read_sql(f"SELECT * FROM target.{table_name}", conn)
#    return df

@asset(
    group_name='training_data',
    #resource_defs={'mlflow': mlflow_tracking},    
    ins={
        "scores_movies_users": AssetIn(
            key=get_asset_key_for_model([db_postgres_dbt_assets], "scores_movies_users"),
        )
    },
    required_resource_keys={"dbt_asset_io_manager"}
)
def training_data(scores_movies_users: pd.DataFrame)-> Output[pd.DataFrame]:
    return scores_movies_users


