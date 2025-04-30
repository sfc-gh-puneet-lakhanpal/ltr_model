import pickle
from snowflake.ml.registry import registry
from starlette.requests import Request
import ray
from typing import Any, Dict, List
from ray import serve
import os
import snowflake.connector
from snowflake.snowpark import Session
import shutil
import os
model_name = os.getenv("MODEL_NAME")
model_download_dir_name = os.getenv("MODEL_DOWNLOAD_DIR_NAME")
# token
def connection() -> snowflake.connector.SnowflakeConnection:
    if os.path.isfile("/snowflake/session/token"):
        creds = {
            'host': os.getenv('SNOWFLAKE_HOST'),
            'port': os.getenv('SNOWFLAKE_PORT'),
            'protocol': "https",
            'account': os.getenv('SNOWFLAKE_ACCOUNT'),
            'authenticator': "oauth",
            'token': open('/snowflake/session/token', 'r').read(),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
            'database': os.getenv('SNOWFLAKE_DATABASE'),
            'schema': os.getenv('SNOWFLAKE_SCHEMA'),
            'client_session_keep_alive': True
        }
    else:
        creds = {
            'account': os.getenv('SNOWFLAKE_ACCOUNT'),
            'user': os.getenv('SNOWFLAKE_USER'),
            'password': os.getenv('SNOWFLAKE_PASSWORD'),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
            'database': os.getenv('SNOWFLAKE_DATABASE'),
            'schema': os.getenv('SNOWFLAKE_SCHEMA'),
            'client_session_keep_alive': True
        }

    connection = snowflake.connector.connect(**creds)
    return connection

def get_session() -> Session:
    return Session.builder.configs({"connection": connection()}).create()

def get_model():
    session = get_session()
    reg = registry.Registry(session=session)
    m = reg.get_model(model_name)
    version_df = m.show_versions()
    last_version_name = version_df['name'].iloc[-1]
    ltr_model = m.version(last_version_name)
    if os.path.exists(f"/models/{model_download_dir_name}/"):
        shutil.rmtree(f"/models/{model_download_dir_name}/")

    os.makedirs(f"/models/{model_download_dir_name}/")

    ltr_model.export(target_path=f"/models/{model_download_dir_name}/")
    file = open(f'/models/{model_download_dir_name}/model/models/{model_name.upper()}/model.pkl', 'rb')
    model = pickle.load(file)
    file.close()
    return model


print("Initializing Ray...")
ray.init(address="auto")
print("Printing Ray cluster resources...")
print(ray.cluster_resources())
model_ref = ray.put(get_model())


@serve.deployment(num_replicas=28, ray_actor_options={"num_cpus": 1}, max_ongoing_requests=1000)
class LTRDeployment:
    def __init__(self, model_ref):
        self.model = ray.get(model_ref)
        print("Model loaded successfully.")

    # Decorator to enable dynamic batching
    @serve.batch(max_batch_size=100, batch_wait_timeout_s=0.01)
    async def handle_batch(self, feature_lists: List[List[List[float]]]) -> List[List[float]]:
        print(f"Handling batch of size: {len(feature_lists)}")
        num_features_per_request = [len(f_list) for f_list in feature_lists]
        combined_features = [item for sublist in feature_lists for item in sublist]
        print(f"Combined features for prediction: {len(combined_features)} vectors")
        predictions = self.model.predict(combined_features)
        print(f"Predictions obtained for batch.")
        results = []
        current_index = 0
        for num_features in num_features_per_request:
            results.append(predictions[current_index : current_index + num_features].tolist())
            current_index += num_features

        print(f"Batch processing complete. Returning {len(results)} results.")
        return results

    async def __call__(self, request: Request) -> List[float]:
        try:
            json_input = await request.json()
            features = json_input.get("features")
            if features is None or not isinstance(features, list):
                raise ValueError("Missing or invalid 'features' key in JSON input.")
            scores: List[float] = await self.handle_batch(features)
            return scores

        except Exception as e:
            print(f"Error processing request: {e}")
            return


app = LTRDeployment.bind(model_ref)
serve.run(app)