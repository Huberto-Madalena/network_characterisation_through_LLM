import pandas as pd
#import os
from typing import List, Dict, Any
from modules.io_utils import export_to_csv
#from modules.aggregation_engine import apply_aggregation
from modules.logic import apply_logic

class StreamProcessor:
    def __init__(self, raw_data: List[Dict[str, Any]], stream_rules: Dict[str, Any]):
        self.raw_data = raw_data
        self.rules = stream_rules
        self.df = pd.DataFrame(raw_data)
        print(f"[+] Stream Processor: loading {len(self.df)} tuple in memory.")

    def process_and_export(self, output_csv_path: str) -> pd.DataFrame:
        self._ensure_numeric_types()
        processed_df = self.df.copy()

        group_by_cols = self.rules.get('group_by', [])
        agg_rules = self.rules.get('aggregate', {})

        if group_by_cols and agg_rules:
            # Hier rufen wir die externe Funktion auf:
            processed_df = apply_logic(processed_df, group_by_cols, agg_rules)

        export_to_csv(processed_df, output_csv_path)
        return processed_df


    def _ensure_numeric_types(self):
        for col in self.df.columns:
            if 'len' in col or 'flags' in col or 'port' in col:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

    def _apply_aggregation(self, df: pd.DataFrame, group_by_cols: List[str], agg_rules: Dict[str, Any]) -> pd.DataFrame:
        print(f"[+] Wende Grouping an nach: {group_by_cols}")
        
        pandas_agg_dict = {}
        

    def _export_to_csv(self, df: pd.DataFrame, output_path: str):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False, sep=';')
        print(f"[+] CSV exported to: {output_path}")
