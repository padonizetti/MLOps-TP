# Sistema de Recomendación MLOps
Este proyecto implementa un pipeline MLOps para un sistema de recomendación utilizando Dagster, Airbyte, DBT, MLflow y Tensorflow. A continuación, se describen los pasos para configurar y desplegar el entorno, instalar dependencias, y ejecutar los componentes necesarios del sistema.

## Configuración del Entorno
Primero, cree un entorno virtual usando Conda y active el entorno:

```bash
conda create -n mlops-tp-pipeline python=3.11
conda activate dagster-airbyte-dbt
```

Instale Dagster:

```bash
pip install dagster==1.6.3
```

## Instalación de Dependencias y Creación de Paquete
Para instalar las dependencias y crear el paquete, utilice el siguiente archivo setup.py:

```python
from setuptools import find_packages, setup
import os

DAGSTER_VERSION=os.getenv('DAGSTER_VERSION', '1.6.3')
DAGSTER_LIBS_VERSION=os.getenv('DAGSTER_LIBS_VERSION', '0.22.3')
MLFLOW_VERSION=os.getenv('MLFLOW_VERSION', '2.10.0')

setup(
    name="recommender_system",
    version="0.0.1",
    packages=find_packages(exclude=["recommender_system_tests"]),
    install_requires=[
        f"dagster=={DAGSTER_VERSION}",
        "dagster-dbt",
        "dbt-postgres",
        f"dagster-airbyte=={DAGSTER_LIBS_VERSION}",
        f"dagster-mlflow=={DAGSTER_LIBS_VERSION}",
        f"mlflow=={MLFLOW_VERSION}",
        "tensorflow==2.14.0",
    ],
    extras_require={
        "dev": ["dagster-webserver", "pytest", "jupyter"], "tests": ["mypy", "pylint", "pytest"]
    },
)
```

Luego, instale el paquete en modo desarrollo junto con las dependencias de desarrollo:

```bash
pip install -e ".[dev]"
```

## Definición de Variables de Entorno
Cree una carpeta environments para las variables de entorno locales, staging y production. Use el archivo local como template. Los secrets reales deben estar en .env, excluido del versionado con .gitignore.

Para establecer las variables de entorno:

```bash
set -o allexport && source .env && set +o allexport
```

Para verificar:

```bash
echo $postgres_data_folder
```

## Deployment de PostgreSQL usando Docker
Para desplegar PostgreSQL:

```bash
docker pull postgres
docker run -d \
    --name mlops-postgres \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v $postgres_data_folder:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres
```

Cree una base de datos y un usuario para MLflow:

```sql
CREATE DATABASE mlflow_db;
CREATE USER mlflow_user WITH ENCRYPTED PASSWORD 'mlflow';
GRANT ALL PRIVILEGES ON DATABASE mlflow_db TO mlflow_user;
```

## Deployment de Airbyte
Clone Airbyte y inicie la plataforma:

```bash
git clone --depth=1 https://github.com/airbytehq/airbyte.git
cd airbyte
./run-ab-platform.sh
```

Acceda a Airbyte en http://localhost:8000/ con el usuario airbyte y contraseña password.

### Creación de Sources en Airbyte
Utilice los siguientes enlaces para crear sources en Airbyte y configure el destino en PostgreSQL. Luego, realice la sincronización inicial.

- [Películas CSV](https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/peliculas_0.csv)
- [Usuarios CSV](https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/usuarios_0.csv)
- [Scores CSV](https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/scores_0.csv)

Nota: Dataset name es el nombre de la tabla que va a tener la data de esta fuente en la base de datos de destino.

### Creación del Destino en Airbyte

Desde el postgres (en docker), se ejecute:

```sql
CREATE DATABASE mlops;
CREATE USER airbyte WITH ENCRYPTED PASSWORD 'airbyte';
GRANT ALL PRIVILEGES ON DATABASE mlops TO airbyte;
GRANT ALL ON SCHEMA public TO airbyte;
GRANT USAGE ON SCHEMA public TO airbyte;
ALTER DATABASE mlops OWNER TO airbyte;
```

Cree conexión en DBeaver y corroborar que está creada la base de datos.
Configure el destino en Airbyte.
Luego creae las conexiones entre las 3 sources y el destino. Luego realice el primer sync para copiar la data en la base de datos.


## DBT

Inicie y configure el proyecto de dbt:

```bash
dbt init db_postgres
```

Configure la base de datos en ~/.dbt/profiles.yml. Al hacer el dbt init le van a solicitar los siguientes datos:

``` yml
dbt_elt:
  outputs:
    dev:
      type: postgres
      threads: 1
      host: localhost
      port: 5432
      user: postgres
      pass: pass
      dbname: mlops
      schema: target
```

Se generan en la carpeta “models” un file schema.yml y los scripts para transformar las tablas movies, users y scores. Finalmente un script que hace el join entre las tablas.
Actualice el archivo dbt_project.yml modificar para que en lugar de vistas, se guarden las transformaciones como tablas:

``` yml
models:
 db_postgres:
   materialized: table
```


## Ejecución de MLflow
Para correr MLflow:

```bash
mlflow server --backend-store-uri postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST/$MLFLOW_POSTGRES_DB --default-artifact-root $MLFLOW_ARTIFACTS_PATH -h 0.0.0.0 -p 5000
```

## Dagster

Para crear el sistema de carpetas puede ejecutar:

```bash
dagster-dbt project scaffold --name recommender_system
```

Inicie Dagster en modo desarrollo:

```bash
dagster dev
```

