import os
import pandas as pd
import psycopg2

from dagster import AssetExecutionContext, asset, AssetIn, AssetOut, Output
from dagster_dbt import DbtCliResource, get_asset_key_for_model
from dagster_dbt import load_assets_from_dbt_project
from dagster_mlflow import mlflow_tracking

from .constants import dbt_project_dir 
#from recommender_system.postgres_config import postgres_host, postgres_port, postgres_user, postgres_password, postgres_db

#@dbt_assets(manifest=dbt_manifest_path)
#def db_postgres_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
#    yield from dbt.cli(["build"], context=context).stream()


dbt_assets = load_assets_from_dbt_project(project_dir=str(dbt_project_dir), 
                                          profiles_dir=str(os.path.expanduser("~/.dbt")))


@asset(compute_kind="python",
       group_name='training_data',
       deps=get_asset_key_for_model(dbt_assets, "scores_movies_users")
       )
def training_data(context: AssetExecutionContext)-> Output[pd.DataFrame]:

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="mlops",
        user="postgres",
        password="mysecretpassword"
    )
    training_data = pd.read_sql("SELECT * FROM target.scores_movies_users", conn)
    
    return Output(training_data)



#  host="localhost", #postgres_host,
#        port="5432", #postgres_port,
#        dbname="mlops", #postgres_db,
#        user="postgres", #postgres_user,
#        password="mysecretpassword" #postgres_password

