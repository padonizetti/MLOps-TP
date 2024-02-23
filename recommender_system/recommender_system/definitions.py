import os
import psycopg2
import pandas as pd

from dagster import Definitions, ScheduleDefinition, define_asset_job, AssetSelection
from dagster_dbt import DbtCliResource
from dagster import load_assets_from_package_module, FilesystemIOManager
from dagster import IOManager, InputContext, OutputContext, InitResourceContext, io_manager
from dagster import job, op, graph, resource, ResourceDefinition

from .dbt import dbt_assets, training_data
from .airbyte import airbyte_assets
from .constants import dbt_project_dir
#from .schedules import schedules
from . import recommender

#from dagster_mlflow import mlflow_tracking

recommender_assets = load_assets_from_package_module(
    package_module=recommender, group_name='recommender'
)

#all_assets = [airbyte_assets, db_postgres_dbt_assets, training_data, *recommender_assets]
all_assets = [airbyte_assets, *dbt_assets, training_data, *recommender_assets]

mlflow_resources = {
    'mlflow': {
        'config': {
            'experiment_name': 'recommender_system',
        }            
    },
}

#data_ops_config = {
#    'db_postgres_dbt_assets': {
#        'config': {
#            'io_manager_key': 'postgres_io_manager'
#            }
#    }
#}

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

job_data_config = {
    'resources': {
        **mlflow_resources,
    },
    'ops': {
        #**data_ops_config,
    }
}

job_training_config = {
    'resources': {
        **mlflow_resources,
    },
    'ops': {
        **training_config
    }
}

job_all_config = {
    'resources': {
        **mlflow_resources,

    },
    'ops': {
        **training_config
    }
}

get_data_job = define_asset_job(
    name='get_data',
    selection=['movies', 'users', 'scores', 'scores_movies_users'],
    config=job_data_config
)

get_data_schedule = ScheduleDefinition(
    job=get_data_job,
    cron_schedule="0 * * * *",  # every hour
)

#@io_manager
#def io_manager_data():
#   return FilesystemIOManager(
#    base_dir="data",  # Path is built relative to where `dagster dev` is run
#    )

#io_manager = FilesystemIOManager(
#    base_dir="data",  # Path is built relative to where `dagster dev` is run
#)

defs = Definitions(
    assets=all_assets,
    jobs=[
        get_data_job,
        define_asset_job("full_process", config=job_all_config),
        define_asset_job(
            "only_training",
            # selection=['preprocessed_training_data', 'user2Idx', 'movie2Idx'],
            selection=AssetSelection.groups('recommender'),
            config=job_training_config
        )
    ],
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir),
                              profiles_dir=str(os.path.expanduser("~/.dbt"))),
        #"io_manager": io_manager,
        #'mlflow': mlflow_tracking
    },
    schedules=[get_data_schedule],
)
