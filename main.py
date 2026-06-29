import os
import sys
from modules.rule_engine import RuleEngine
from modules.pcap_processor import run_data_plane
from modules.data_exporter import StreamProcessor
from modules.llm_analyzer import analyze_network_data
from modules.io_utils import export_to_csv


def main():
    print("===  Network Characterization Pipeline ===")
    
    # paths to main files
#consider  changing static paths to user prompts for pcap file and google API key
    config_path = "config/rules.yaml"
    pcap_file = "data/input_pcaps/sample.pcap" 
    output_csv = "data/output/characterization.csv"
    
    # Step 1: set query
    query_id = "ultimate_audit" 
    
    #  Step 2: set rule engine in order to apply network feature generalisation
    engine = RuleEngine(config_path)
    #engine = RuleEngine("config/rules.yaml")
    plan = engine.get_query_plan(query_id)

    # --- Step 3: feature extraction. variable raw_tuples combines pcap file and generalisation rules 
    print("\n--- feature extraction in a structured manner ---")
    raw_tuples = run_data_plane(pcap_file, plan['data_plane_rules'])
    

    # --- step 2: use stream processor to bring up the logic behind the selection of relevant flows
    print("\n--- Starting Stream Processor ---")
    
    # the logic for stream processing is outsourced in the respective file
#consider alterations in order to improve the logic
    import yaml
    with open("config/stream_processor.yaml", "r") as f:
        stream_config = yaml.safe_load(f)["stream_processor"]
    
    # use loaded stream config
# stream processor also produces the CSV output file. consider a new file for this to improve modularity
    processor = StreamProcessor(raw_tuples, stream_config)
    final_df = processor.process_and_export(output_csv)
    
    print("\n=== pcap info loaded onto csv file ===")
    print(final_df.head(10).to_string())
    
    # --- Step 3. characterisation through LLM
    #use analyse_network_data from llm module, with output_csv and plan as params
    print("\n--- Starting LLM analysis ---")
    llm_report = analyze_network_data(output_csv, plan['query_id'])
    
    print("\n" + "="*30)
    print(llm_report)
    print("="*30)

    
    #print("\n=== analysis over ===")

main()
