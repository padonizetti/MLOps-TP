import os
from pathlib import Path

from dagster_dbt import DbtCliResource

dbt_project_dir = Path(__file__).joinpath("..", "..", "..", "db_postgres").resolve()
dbt = DbtCliResource(project_dir=os.fspath(dbt_project_dir))

# If DAGSTER_DBT_PARSE_PROJECT_ON_LOAD is set, a manifest will be created at run time.
# Otherwise, we expect a manifest to be present in the project's target directory.
if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD"):
    dbt_manifest_path = (
        dbt.cli(
            ["--quiet", "parse"],
            target_path=Path("target"),
        )
        .wait()
        .target_path.joinpath("manifest.json")
    )
else:
    dbt_manifest_path = dbt_project_dir.joinpath("target", "manifest.json")

# Airbyte configs
AIRBYTE_CONNECTION_ID = os.environ.get("AIRBYTE_CONNECTION_ID", "ff2795fa-7a13-4477-b955-3ddde02ea68f")


AIRBYTE_CONFIG = {
    "host": os.environ.get("AIRBYTE_HOST", "localhost"),
    "port": os.environ.get("AIRBYTE_PORT", "8000"),
    "username":  "airbyte", 
    "password":  "password",
}

#
