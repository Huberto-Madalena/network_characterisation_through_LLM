# modules/Logic.py
import pandas as pd
from typing import List, Dict, Any

def apply_logic(df: pd.DataFrame, group_by_cols: List[str], agg_rules: Dict[str, Any]) -> pd.DataFrame:
    """
    conduct aggregation based on yaml file rules.
    """
    pandas_agg_dict = {}

    # aggregation logic
#look for these specific values:  "fields" and "function" in agg_rules function in order to build dictionary for agrgegated values
    if 'fields' in agg_rules and 'function' in agg_rules:
        func = agg_rules['function']
        for field in agg_rules['fields']:
            if field in df.columns:
                pandas_agg_dict[field] = func

    elif 'field' in agg_rules and 'function' in agg_rules:
        field = agg_rules['field']
        func = agg_rules['function']
        if func == 'distinct':
            func = 'nunique'
        if field in df.columns:
            pandas_agg_dict[field] = func

    if pandas_agg_dict:
        # grouping up values. 
#fillna(0) is used in Pandas in order to handle invalid or missing values, replacing them with 0
        df = df.fillna(0).groupby(group_by_cols).agg(pandas_agg_dict).reset_index()
        print(f"[+] Aggregation carried out to completion. Reduction: {len(df)} cells.")

    return df
