import pandas as pd

def add_payload_efficiency_metrics(df_flows: pd.DataFrame) -> pd.DataFrame:
    """
    calculate payload-efficiency and average packet size
	this logic helps select the relevant flows that shall be interpreted by the LLM model for network characterisaion
    """
    if 'total_frame_bytes' in df_flows.columns:
        # with total_frame_bytes in our aggregation file, we can calculate the payload efficiency by using the ratio of total size in relation to total payload
        df_flows['payload_percentage'] = (
            df_flows['total_payload']
            / df_flows['total_frame_bytes'].replace(0, 1)
        ) * 100

        df_flows['payload_percentage'] = (
            df_flows['payload_percentage']
            .round(2)
            .clip(lower=0)
        )

        # average packet size
        df_flows['avg_packet_size'] = (
            df_flows['total_frame_bytes']
            / df_flows['packet_count'].replace(0, 1)
        ).round(2)
    
    return df_flows
