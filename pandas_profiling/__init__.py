import sys
import warnings
import json
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np

from pandas_profiling.config import config
from pandas_profiling.describe import describe as describe_df


class ProfileReport(object):

    def __init__(self, df):

        self.date = datetime.now()
        # Rename reserved column names
        df = self.rename_index(df)
        # Remove spaces and colons from column names
        df = self.clean_column_names(df)
        # Sort names according to config (asc, desc, no sort)
        df = self.sort_column_names(df)
        config["column_order"] = df.columns.tolist()
        # Get dataset statistics
        self.description_set = describe_df(df)
        # Build report structure
        self.sample = self.get_sample(df)
        self.title = config["title"].get(str)
        
    def sort_column_names(self, df):
        sort = config["sort"].get(str)
        if sort in ["asc", "ascending"]:
            df = df.reindex(sorted(df.columns, key=lambda s: s.casefold()), axis=1)
        elif sort in ["desc", "descending"]:
            df = df.reindex(
                reversed(sorted(df.columns, key=lambda s: s.casefold())), axis=1
            )
        elif sort != "None":
            raise ValueError('"sort" should be "ascending", "descending" or None.')
        return df
    
    def clean_column_names(self, df):
        df.columns = df.columns.str.replace(" ", "_")
        df.columns = df.columns.str.replace(":", "")
        return df


    def rename_index(self, df):
        df.rename(columns={"index": "df_index"}, inplace=True)

        if "index" in df.index.names:
            df.index.names = [x if x != "index" else "df_index" for x in df.index.names]
        return df

    def get_sample(self, df: pd.DataFrame) -> dict:
        sample = {}
        sample["head"] = df.head(n=10)
        sample["tail"] = df.tail(n=10)
        return sample
