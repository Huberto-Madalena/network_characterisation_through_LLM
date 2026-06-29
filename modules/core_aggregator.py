import pandas as pd
from typing import List, Dict, Any
# Importing dependencies
from modules.payload_efficiency import add_payload_efficiency_metrics

def execute_core_aggregation(
    df: pd.DataFrame, 
    group_by_cols: List[str], 
    pandas_agg_dict: Dict[str, Any]
) -> pd.DataFrame:
    """
    Führt die gesamte Aggregations-Pipeline aus.
    """
    # fill in numeric data with 0 for initial setup!
    # the code uses the function fillna() in order to replace missing values with 0
     
    df_filled = df.copy()
    numeric_cols = df_filled.select_dtypes(include='number').columns
    df_filled[numeric_cols] = df_filled[numeric_cols].fillna(0)

    # 1. Main aggregation
    df_flows = (
        df_filled
        .groupby(group_by_cols)
        .agg(pandas_agg_dict)
        .reset_index()
    )

    # 2. Packet count processing
    counts = (
        df_filled
        .groupby(group_by_cols)
        .size()
        .reset_index(name='packet_count')
    )
    df_flows = pd.merge(df_flows, counts, on=group_by_cols)

    # 3. Add total size, in case it's present
    if 'frame.len' in df.columns:
        frame_totals = (
            df_filled
            .groupby(group_by_cols)['frame.len']
            .sum()
            .reset_index(name='total_frame_bytes')
        )
        df_flows = pd.merge(df_flows, frame_totals, on=group_by_cols)

    # 4. Payload-calc
    tcp_payload = df_flows.get('tcp.len', pd.Series(0, index=df_flows.index)).fillna(0)
    udp_payload = df_flows.get('udp.length', pd.Series(0, index=df_flows.index)).fillna(0)
    df_flows['total_payload'] = tcp_payload + udp_payload

    # 5. call on payload efficiency logic
    df_flows = add_payload_efficiency_metrics(df_flows)

    # 6. sorting in descending order
    df_flows = df_flows.sort_values(
        by=['total_payload', 'payload_percentage'],
        ascending=[False, False]
    )

    print(f"[+] Aggregation & Pipeline carried out to completion. Reduction {len(df_flows)} cells.")

    return df_flows
