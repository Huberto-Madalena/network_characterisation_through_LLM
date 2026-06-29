import os
import pandas as pd

def export_to_csv(df: pd.DataFrame, output_path: str):
    """
    Hilfsfunktion: Speichert das DataFrame als CSV und erstellt nötige Verzeichnisse.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, sep=';')
    print(f"[+] CSV erfolgreich exportiert nach: {output_path}")
