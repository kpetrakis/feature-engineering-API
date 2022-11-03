import src.config as config
import pandas as pd
import json


def load_data_from_json():
  with open(config.data_path, "r") as f:
    entries = json.load(f)["data"]
  df = pd.DataFrame.from_dict(entries)
  return df

def load_and_preprocess():
  df = load_data_from_json()
  # split in 2 DataFrames, for featuretools dfs
  customers_df = df.copy()
  loans_df = df["loans"]

  customers_df["annual_income"] = customers_df.apply(lambda x: 
  float(x["loans"][0]["annual_income"]), axis=1)
  customers_df.drop(["loans"], axis=1,errors="ignore", inplace=True)

  loans_df = loans_df.explode()
  loans_df = pd.json_normalize(loans_df)
  loans_df .drop(["annual_income"], axis=1, errors="ignore", inplace=True)
  # i get IndexError: Index column must be unique on featuretool.dfs() without this:
  loans_df = loans_df.rename_axis("loan_id").reset_index().astype(str)
  # xreiazetai mia stili san unique index!!

  # object type -> appropiate format
  loans_df["loan_date"] = pd.to_datetime(loans_df["loan_date"],dayfirst=True)
  loans_df["ammount"] = loans_df["amount"].apply(pd.to_numeric)
  loans_df["fee"] = loans_df["fee"].apply(pd.to_numeric)

  return customers_df, loans_df

