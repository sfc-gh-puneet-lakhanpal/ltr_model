
from locust import User, task, between
from accessviakeypair import get_jwt
import logging
import json
import requests
import os
import sys
import json
account = "sfsenorthamerica-demo391"
user = "kipi_ltr_user"
private_key_file_path = "./rsa_key.p8"
endpoint = "nu64aqc-sfsenorthamerica-demo391.snowflakecomputing.app"
role = "kipi_ltr_role"
endpoint_path = "/predict"
spcs_url=f'https://{endpoint}{endpoint_path}'
data = {'data': [[0, 1.0, 0.0, 39.0, 79275.83, 790.0, 1.0, 500.0, 100.0, 0.0, 34855.0, 290.0, 44420.83, 2.27444642088653, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0]]}


jwt = get_jwt(account, user, private_key_file_path, endpoint, role)
print(jwt)
def classify(token, url, data):
  # Create a request to the ingress endpoint with authz.
  headers = {'Authorization': f'Snowflake Token="{token}"'}
  response = requests.post(url,  json=data, headers=headers)
  return response.text
class ClassificationUser(User):
    @task
    def generation(self):
        # Invoke the model
        with self.environment.events.request.measure("[Send]", "Morgage Classification REST API performance authenticated with JWT"):
            results = classify(token=jwt, url=spcs_url, data=data)
            logging.info(results)
                  
