import streamlit as st
import pandas as pd
from layout import app_layout

def main():

  @st.cache_data
  def load_csv():
      
      data_set = pd.read_csv("data/cleaned_recipes_v2.csv")
      return data_set

  data_set = load_csv()

  print("BEGINNING OF THE DASHBOARD")

  app_layout()
  

if __name__ == '__main__':
    main()

