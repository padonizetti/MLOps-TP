import os

from dagster import Definitions, ScheduleDefinition, define_asset_job
from dagster_dbt import DbtCliResource
from dagster import load_assets_from_package_module, FilesystemIOManager

from .dbt import db_postgres_dbt_assets
from .airbyte import airbyte_assets
from .constants import dbt_project_dir
from .schedules import schedules
from . import recommender

from dagster_mlflow import mlflow_tracking

recommender_assets = load_assets_from_package_module(
    package_module=recommender, group_name='recommender'
)

mlflow_resources = {
    'mlflow': {
        'config': {
            'experiment_name': 'recommender_system',
        }            
    },
}

training_config = {
    'keras_dot_product_model': {
        'config': {
            'batch_size': 128,
            'epochs': 10,
            'learning_rate': 1e-3,
            'embeddings_dim': 5
        }
    }
}

#io_manager = FilesystemIOManager(
#    base_dir="data",  # Path is built relative to where `dagster dev` is run
#)


defs = Definitions(
    assets=[db_postgres_dbt_assets, airbyte_assets, *recommender_assets],
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
        #'mlflow': mlflow_tracking
    },
    schedules=[
        # update all assets once a day
        ScheduleDefinition(
            job=define_asset_job("all_assets", selection="*"), cron_schedule="@daily"
        ),
    ],
)
