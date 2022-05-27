import os

import pandas as pd

os.chdir(os.path.join(os.getcwd(), "../data/raw"))

for dado in [
    "portfolio_clientes",
    "portfolio_comunicados",
    "portfolio_tpv",
    "portfolio_geral",
]:
    df = pd.read_csv(f"{dado}.csv")
    df.to_parquet(f"{dado}.parquet")
