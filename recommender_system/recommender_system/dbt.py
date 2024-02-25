import os
import pandas as pd
import psycopg2

from dagster import AssetExecutionContext, asset, Output
from dagster_dbt import get_asset_key_for_model
from dagster_dbt import load_assets_from_dbt_project

from .constants import dbt_project_dir 

postgres_host, postgres_port = os.getenv("POSTGRES_HOST").split(":")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_db = os.getenv("MLOPS_POSTGRES_DB")


dbt_assets = load_assets_from_dbt_project(project_dir=str(dbt_project_dir), 
                                          profiles_dir=str(os.path.expanduser("~/.dbt")))


@asset(compute_kind="python",
       group_name='training_data',
       deps=get_asset_key_for_model(dbt_assets, "scores_movies_users")
       )
def training_data(context: AssetExecutionContext)-> Output[pd.DataFrame]:

    conn = psycopg2.connect(
        host=postgres_host,
        port=postgres_port,
        dbname=postgres_db,
        user=postgres_user,
        password=postgres_password
    )
    training_data = pd.read_sql("SELECT * FROM target.scores_movies_users", conn)
    
    return Output(training_data)

