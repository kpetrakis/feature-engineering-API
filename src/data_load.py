import src.config as config
import pandas as pd
import json

class DataLoader():
  def __init__(self):
    self.data_path = config.data_path
    self.customers_df = None
    self.loans_df = None
  
  def load_data_from_json(self):
    with open(self.data_path, "r") as f:
      entries = json.load(f)["data"]
    df = pd.DataFrame.from_dict(entries)
    return df

  def load_data(self):
    df = self.load_data_from_json()
    #split in 2 DataFrames for featuretools dfs
    self.customers_df = df.copy()
    self.loans_df = df["loans"]
    return self.customers_df, self.loans_df

  def preprocess(self):
    self.customers_df["annual_income"] = self.customers_df.apply(lambda x: 
    float(x["loans"][0]["annual_income"]), axis=1)
    self.customers_df.drop(["loans"], axis=1,errors="ignore", inplace=True)

    self.loans_df = self.loans_df.explode()
    self.loans_df = pd.json_normalize(self.loans_df)
    self.loans_df .drop(["annual_income"], axis=1, errors="ignore", inplace=True)
    # i get IndexError: Index column must be unique on featuretool.dfs() without this:
    self.loans_df = self.loans_df.rename_axis("loan_id").reset_index().astype(str)
    # xreiazetai mia stili san unique index!!

    # object type -> appropiate format
    self.loans_df["loan_date"] = pd.to_datetime(self.loans_df["loan_date"],dayfirst=True)
    self.loans_df["ammount"] = self.loans_df["amount"].apply(pd.to_numeric)
    self.loans_df["fee"] = self.loans_df["fee"].apply(pd.to_numeric)

    return self.customers_df, self.loans_df

# def load_data_from_json():
#   with open(config.data_path, "r") as f:
#     entries = json.load(f)["data"]
#   df = pd.DataFrame.from_dict(entries)
#   return df

# def load_and_preprocess():
#   df = load_data_from_json()
#   # split in 2 DataFrames, for featuretools dfs
#   customers_df = df.copy()
#   loans_df = df["loans"]

#   customers_df["annual_income"] = customers_df.apply(lambda x: 
#   float(x["loans"][0]["annual_income"]), axis=1)
#   customers_df.drop(["loans"], axis=1,errors="ignore", inplace=True)

#   loans_df = loans_df.explode()
#   loans_df = pd.json_normalize(loans_df)
#   loans_df .drop(["annual_income"], axis=1, errors="ignore", inplace=True)
#   # i get IndexError: Index column must be unique on featuretool.dfs() without this:
#   loans_df = loans_df.rename_axis("loan_id").reset_index().astype(str)
#   # xreiazetai mia stili san unique index!!

#   # object type -> appropiate format
#   loans_df["loan_date"] = pd.to_datetime(loans_df["loan_date"],dayfirst=True)
#   loans_df["ammount"] = loans_df["amount"].apply(pd.to_numeric)
#   loans_df["fee"] = loans_df["fee"].apply(pd.to_numeric)

#   return customers_df, loans_df

