import pandas as pd
from typing import List, Dict, Any
# core logic
from modules.core_aggregator import execute_core_aggregation

def execute_aggregation(
    df: pd.DataFrame,
    group_by_cols: List[str],
    pandas_agg_dict: Dict[str, Any]
) -> pd.DataFrame:
    #check whether there is overall something to be aggregated; namely, if the dictionary with the data assembled data is available
    #if not pandas_agg_dict:
    #    print("[-] no fields that suit the aggregation criteria found.")
    #    return df

    # delegating processing work to imported function
    return execute_core_aggregation(df, group_by_cols, pandas_agg_dict)
