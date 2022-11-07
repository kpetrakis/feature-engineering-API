from fastapi import FastAPI
from fastapi.testclient import TestClient
import json 
# import src.config as config
from src.data_load import DataLoader
from src.feature_engineering import FeatureEngineer
import src.config as config

app = FastAPI()
client = TestClient(app)


@app.get("/")
def read_root():
  return {"Hello": "My name is Kostis and this is my API implementation"}

@app.get("/api/api_status")
def fetch_api_status():
  response_root = client.get("/")
  response_customers = client.get("/api/features/customers")
  response_loans = client.get("/api/features/loans")
  try:
    assert response_root.status_code == 200
    assert response_customers.status_code == 200
    assert response_loans.status_code == 200
    return {"status": "UP"}
  except Exception as e:
    return {"status":"DOWN"}

@app.get("/api/features/customers")
def fetch_customers_features():

  data_loader = DataLoader() 
  customers_df, loans_df = data_loader.load_data()
  customers_df, loans_df = data_loader.preprocess()

  feature_engineer = FeatureEngineer()
  feature_engineer.add_dataframe("customers", customers_df, "customer_ID")
  feature_engineer.add_dataframe("loans", loans_df, "") 
  # an edw perasw to loan_id pernw diaforetika result... GIATI??
  feature_engineer.add_relationship("customers","customer_ID","loans","customer_ID")

  customers_features_df, _ = feature_engineer.dfs("customers") 

  feature_engineer.store_features(customers_features_df,config.features_customers_path)
  
  customers_features_json = customers_features_df.to_json(orient="records")
  customers_features = json.loads(customers_features_json)

  return customers_features

@app.get("/api/features/loans")
def fetch_loans_features():
  data_loader = DataLoader()
  customers_df, loans_df = data_loader.load_data()
  customers_df, loans_df = data_loader.preprocess()

  feature_engineer = FeatureEngineer()
  feature_engineer.add_dataframe("customers", customers_df, "customer_ID")
  feature_engineer.add_dataframe("loans", loans_df, "") 
  # an edw perasw to loan_id pernw diaforetika result... GIATI??
  feature_engineer.add_relationship("customers","customer_ID","loans","customer_ID")

  loans_features_df, _ = feature_engineer.dfs("loans") 

  feature_engineer.store_features(loans_features_df,config.features_loans_path)
  
  loans_features_json = loans_features_df.to_json(orient="records")
  loans_features = json.loads(loans_features_json)

  return loans_features

@app.get("/api/customers/{customer_id}")
def fetch_annual_income_for_customer(customer_id):
  '''
  return the customer id with the annual income
  '''
  data_loader = DataLoader()
  customers_df, _  = data_loader.load_data()
  customers_df, _ = data_loader.preprocess()

  customer_id = customers_df.loc[customers_df["customer_ID"]==customer_id]  
  if customer_id.empty:
    return {"Sorry":"This customer_ID doesn't exist"}
  else:
    customer_id_json = customer_id.to_json(orient="records")
    customer_id_res = json.loads(customer_id_json)
    return customer_id_res 

@app.get("/api/loans/{customer_id}")
def fetch_loan_with_customer_id(customer_id: str):
  '''
  return the loan entry corresponding to the customer_id
  '''
  data_loader = DataLoader()
  _, loans_df  = data_loader.load_data()
  _, loans_df = data_loader.preprocess()
  
  customer_id = loans_df.loc[loans_df["customer_ID"]==customer_id]
  if customer_id.empty:
    return {"Sorry":"This customer_ID doesn't exist"}
  else:
    customer_id_json = customer_id.to_json(orient="records")
    customer_id_res = json.loads(customer_id_json)
    return customer_id_res 

@app.get("/api/features/customers/{customer_id}")
def fetch_customer_features_with_customer_id(customer_id):
  '''
  return the customer features with the given customer_id
  '''
  data_loader = DataLoader() 
  customers_df, loans_df = data_loader.load_data()
  customers_df, loans_df = data_loader.preprocess()

  feature_engineer = FeatureEngineer()
  feature_engineer.add_dataframe("customers", customers_df, "customer_ID")
  feature_engineer.add_dataframe("loans", loans_df, "") 
  # an edw perasw to loan_id pernw diaforetika result... GIATI??
  feature_engineer.add_relationship("customers","customer_ID","loans","customer_ID")

  customers_features_df, _ = feature_engineer.dfs("customers") 
  customer_id = customers_features_df.loc[customers_df['customer_ID']==customer_id]
  # index me to customers_df !!!
  if customer_id.empty:
    return {"Sorry":"This customer_ID doesn't exist"}
  else:
    customer_id_json = customer_id.to_json(orient="records")
    customer_id_res = json.loads(customer_id_json)
    return customer_id_res 

@app.get("/api/features/loans/{customer_id}")
def fetch_loan_features_with_customer_id(customer_id: str):
  '''
  return the loan features with the customer_id
  '''
  data_loader = DataLoader()
  customers_df, loans_df = data_loader.load_data()
  customers_df, loans_df = data_loader.preprocess()

  feature_engineer = FeatureEngineer()
  feature_engineer.add_dataframe("customers", customers_df, "customer_ID")
  feature_engineer.add_dataframe("loans", loans_df, "") 
  # an edw perasw to loan_id pernw diaforetika result... GIATI??
  feature_engineer.add_relationship("customers","customer_ID","loans","customer_ID")

  loans_features_df, _ = feature_engineer.dfs("loans") 
  customer_id = loans_features_df.loc[loans_df["customer_ID"]==customer_id]
  # index me to loans_df !!!
  if customer_id.empty:
    return {"Sorry":"This customer_ID doesn't exist"}
  else:
    customer_id_json = customer_id.to_json(orient="records")
    customer_id_res = json.loads(customer_id_json)
    return customer_id_res 