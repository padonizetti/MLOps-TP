# %% 
import os
import psycopg2

import pandas as pd
from recommender_system.postgres_config import postgres_host, postgres_port, postgres_user, postgres_password, postgres_db

print("postgres_host:", postgres_host)
print("postgres_port:", postgres_port)
print("postgres_user:", postgres_user)
print("postgres_password:", postgres_password)
print("postgres_db:", postgres_db)

# %%
def training_data():
    
    print("postgres_host:", postgres_host)
    print("postgres_port:", postgres_port)
    print("postgres_user:", postgres_user)
    print("postgres_password:", postgres_password)
    print("postgres_db:", postgres_db)
    
    conn = psycopg2.connect(
        host=postgres_host,
        port=postgres_port,
        dbname=postgres_db,
        user=postgres_user,
        password=postgres_password
    )
    df = pd.read_sql("SELECT * FROM target.scores_movies_users", conn)
    return df
# %%

data = training_data()

print(data.head())


# %%
