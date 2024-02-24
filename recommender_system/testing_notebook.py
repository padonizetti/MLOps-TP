# %%
import mlflow
import os

os.environ['MLFLOW_TRACKING_URI'] = 'http://localhost:5000'
mlflow_tracking_uri = os.environ.get('MLFLOW_TRACKING_URI')
print(mlflow_tracking_uri)

# %%
logged_model = 'models:/keras_dot_product_model/1'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)
# %%

# %%
# Predict on a Pandas DataFrame.
import numpy as np
loaded_model.predict([np.array([1, 2]), np.array([2, 3])])
# %%
# %%
mlflow.set_experiment('test')
# %%
# %%
mlflow.start_run()
# %%
from tensorflow.keras import layers, Model
# %%
input = layers.Input(shape=(1,))
dense = layers.Dense(10)(input)
model = Model(input, dense)
# %%
model.summary()
# %%
logged_model = mlflow.tensorflow.log_model(
        model,
        "simple",
        registered_model_name='simple'
    )
# %%
logged_model.__dir__()
# %%

# %%
{
    'model_uri': logged_model.model_uri,
    'run_id': logged_model.run_id
}
# %%
logged_model.flavors
# %%
