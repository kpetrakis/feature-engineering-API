import src.config as config
import src.data_load as data_load
import pandas as pd
import featuretools as ft


def store_features(features_df, path):
  '''
  gia na kanw store ta apotelesmata tou feture engineering se morfi json
  '''
  features_df.to_json(path,orient="records") # records gia na einai pio readable

def dfs(customers_df, loans_df):
  '''
  Featuretools deep feature search
  '''
  relationship = [("customers", "customer_ID", "loans", "customer_ID")]
  dataframes = dict()

  dataframes["customers"] = (customers_df,"customer_ID")
  dataframes["loans"] = (loans_df,)

  customers_feature_matrix, customers_feature_defs = ft.dfs(
    dataframes, relationships=relationship,target_dataframe_name="customers"
  )
  loans_feature_matrix, loans_feature_defs = ft.dfs(
    dataframes, relationships=relationship,target_dataframe_name="loans"
  )
  return customers_feature_matrix, loans_feature_matrix

# debugging
if __name__ == "__main__":
  customers_df, loans_df = data_load.load_and_preprocess()
  customers_features, loans_features = dfs(customers_df,loans_df)
  
  store_features(customers_features, config.features_customers_path)
  store_features(loans_features, config.features_loans_path)

  print(customers_features.head())
  print(loans_features.head())