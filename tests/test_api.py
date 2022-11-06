from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.main import app
import json

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



if __name__ == "__main__":
  print("Testing customers features:")
  test_features_customers()

  print("Testing loans features: ")
  test_features_loans()