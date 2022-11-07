from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_features_customers():
  response = client.get("/api/features/customers")
  print(response.json()) # list of dicts

  try:
    assert response.status_code == 200
  except Exception as e:
    raise e

def test_features_loans():
  response = client.get("/api/features/loans")
  print(response.json())

  try:
    assert response.status_code == 200
  except Exception as e:
    raise e

def test_fetch_customer(customer_id):
  '''
  i test on the first customer id
  '''
  response = client.get("/api/customers/1090")

  try:
    assert response.status_code == 200
    assert response.json()[0]["customer_ID"] == "1090"
    assert response.json()[0]["annual_income"] == 41333
  except Exception as e:
    raise e

def test_fetch_loan(customer_id):
  '''
  teston the first customer_ID
  '''
  response = client.get("/api/loans/1090")
  try:
    assert response.status_code == 200
    assert response.json()[0]["loan_id"] == "0"
    assert response.json()[0]["ammount"] == 2426.
    assert response.json()[0]["fee"] == 199
    assert response.json()[0]["term"] == "long"
    assert response.json()[0]["loan_status"] == "0"
  except Exception as e:
    raise e


if __name__ == "__main__":
  print("Testing customers features:")
  test_features_customers()

  print("Testing loans features: ")
  test_features_loans()
  
  print("Test fetch customer with id 1090:")
  test_fetch_customer("1090")
  
  print("Test fetch loan with customer_ID=1090:")
  test_fetch_loan("1090")