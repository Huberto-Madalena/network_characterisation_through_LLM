import pandas as pd
import typing Dict, List, Any

       #  Aggregation logic. look for the values 'fields' and 'function' in agg_rules function in order to assemble aggregation dictionary
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

       # if pandas_agg_dict:
       #     df = df.fillna(0).groupby(group_by_cols).agg(pandas_agg_dict).reset_index()
       #     print(f"[+] Aggregation concluded, with {len(df)} cell reduction.")

        return df
