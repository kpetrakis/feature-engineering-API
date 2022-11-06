import src.config as config
from src.data_load import DataLoader
import pandas as pd
import featuretools as ft

class FeatureEngineer():
  def __init__(self):
    self.dataframes = dict()
    self.relationships = []
    self.primitives = ["sum", "std", "max", "min", "mean", "count", "percent_true","num_unique", "mode"] 
    # skew produces lots of nulls
    # std too on some features but i let in...

  def store_features(self, features_df, path):
    '''
    gia na kanw store ta apotelesmata tou feature engineering se morfi json
    '''
    features_df.to_json(path,orient="records")
    # records gia na einai pio readable

  def add_dataframe(self, df_name, df, index_col):
    self.dataframes[df_name] = (df, index_col)

  def add_relationship(self,parent_df, parent_col, child_df, child_col):
    '''
    maybe i can pass it in as a tuple or implement both ways..
    '''
    relationship = (parent_df, parent_col, child_df, child_col)
    self.relationships.append(relationship)

  def dfs(self,target_df_name):
    '''
    > Featuretools deep feature search

    > i only pass the target_df_name, since its the only thing
    changing between the two calls
    '''
    
    feature_matrix, feature_defs = ft.dfs(
      self.dataframes, relationships=self.relationships,
      agg_primitives = self.primitives,
      target_dataframe_name=target_df_name
    ) 
    return feature_matrix, feature_defs # ->for debug only?


# debugging
if __name__ == "__main__":
  data_loader = DataLoader()
  customers_df, loans_df = data_loader.load_data()
  customers_df, loans_df = data_loader.preprocess()

  feature_engineer = FeatureEngineer()
  feature_engineer.add_dataframe("customers", customers_df, "customer_ID")
  feature_engineer.add_dataframe("loans", loans_df,"") 
  # an edw perasw to loan_id pernw diaforetika result... GIATI??
  feature_engineer.add_relationship("customers","customer_ID","loans","customer_ID")

  customers_features, _ = feature_engineer.dfs("customers") 

  loans_features, _ = feature_engineer.dfs("loans")

  feature_engineer.store_features(customers_features,config.features_customers_path)
  feature_engineer.store_features(loans_features, config.features_loans_path)

  print(customers_features.head())
  print(loans_features.head())