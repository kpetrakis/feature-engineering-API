from fastapi import FastAPI
from fastapi.testclient import TestClient
import json 
# import src.config as config
import src.data_load as data_load
import src.feature_engineering as feature_engineering

app = FastAPI()
client = TestClient(app)


@app.get("/")
def read_root():
  return {"Hello": "My name is Kostis and this is my API implementation"}

@app.get("/api/api_status")
def fetch_api_status():
  response = client.get("/")
  try:
    assert response.status_code == 200
    return {"status": "UP"}
  except Exception as e:
    return {"status":"DOWN"}

@app.get("/api/features/customers")
def fetch_customers_features():
  
  customers_df, loans_df = data_load.load_and_preprocess()

  customers_features_df , _ = feature_engineering.dfs(
    customers_df, loans_df
  )

  # feature_engineering.store_features(customers_features, config.features_customers_path)
  
  customers_features_json = customers_features_df.to_json(orient="records")
  customers_features = json.loads(customers_features_json)

  return customers_features

@app.get("/api/features/loans")
def fetch_loans_features():
  customers_df, loans_df = data_load.load_and_preprocess()

  _, loans_features_df = feature_engineering.dfs(
    customers_df, loans_df
  )
  # feature_engineering.store_features(loans_features, config.features_loans_path)
  loans_features_json = loans_features_df.to_json(orient="records")
  loans_features = json.loads(loans_features_json)

  return loans_features

  