import pandas as pd
import numpy as np
import os
# importing model for outsourced logic
from modules.llm_client import generate_ai_analysis

def analyze_network_data(csv_path: str, query_description: str) -> str:
    """
read agrgegated data, calculate combined score from volume and overhead and hand over top 100 most relevant flows according to this relevance score to the llm model
    """
    print(f"\n[+] LLM Analyzer: reading aggregate network data from {csv_path}")
    
    df = pd.read_csv(csv_path, sep=';')

    # starting llm pipeline
    # --- 1. Payload & Absolute Wasted Bytes ---
    tcp_payload = df['tcp.len'].fillna(0)
    udp_payload = df['udp.length'].fillna(0)
    total_payload = tcp_payload + udp_payload

    df['wasted_bytes'] = df['frame.len'] - total_payload
    df['wasted_bytes'] = df['wasted_bytes'].clip(lower=0.0)

    # --- 2. overhead % calc ---
    df['overhead_percentage'] = (df['wasted_bytes'] / df['frame.len']) * 100
    df['overhead_percentage'] = df['overhead_percentage'].replace([np.inf, -np.inf], 100.0).fillna(0.0)
    df['overhead_percentage'] = df['overhead_percentage'].clip(0.0, 100.0)

    # --- 3. Normalisation and relevance score ---
    max_frame = df['frame.len'].max() if df['frame.len'].max() > 0 else 1
    max_waste = df['wasted_bytes'].max() if df['wasted_bytes'].max() > 0 else 1

    df['norm_volume'] = df['frame.len'] / max_frame
    df['norm_waste'] = df['wasted_bytes'] / max_waste
    df['relevance_score'] = (df['norm_volume'] + df['norm_waste']) / 2

    # --- 4. sort out according to new combined score ---
    if 'relevance_score' in df.columns:
        df = df.sort_values(by='relevance_score', ascending=False)

    if len(df) > 100:
        print("[*]  Sending Top 100 Flows based on relevance score for length, payload and overhead LLM.")
        df_subset = df.head(100)
    else:
        df_subset = df
    #rounding off float values for a cleaner csv transfer
    
    df_subset = df_subset.round(2)
    csv_string = df_subset.to_csv(index=False, sep=';')

    # ---  Prompt ---
    system_prompt = (
        "As a Smart AI system for a monitoring system, you are to provide answers to common netadmins' questions. "
        "by analysing aggregated flow data, generate  professional, albeit brief status report for the system administrator. "
        "The data is sorted in descending order taking into account the mean between size, overhead and payload. "
        "pay attention to lots of protocol headers but little to no payload (typical for scans, handshakes, keep-alives, or attacks).\n\n"
        "response in Markdown and include these  sections:\n"
        "1. Security analysis: max 2 sentences and 60 words. Analyze the high-overhead flows for scan vulnerabilities or attacks (XMAS: FIN, PSH, URG > 0. FIN-Scan: FIN>0, ACK=0. Semi-open: SYN>0, ACK=0).be to the point and brief\n"
        "2 QoS heads-up: Analyse the flow for signs of jitter, thourghput, latency and other Quality of service stats. brevity and max 2 sentences \n"
        "3. High-Overhead & Anomalous Flows: Identify the top talkers in terms of overhead. max 1 sentence \n"
        "4. Services & Protocol Analysis: Which destination ports (tcp.dstport / udp.dstport) dominate these high-overhead connections? Are they legitimate keep-alives or suspicious traffic?\n"
        "5. Routing & Health: Check for routing anomalies using ip.ttl/ipv6.hlim or ICMP errors within these specific flows.max 2 sentences \n"
        "6. Analyse and include switch-related data. Look for packets containing STP, vlan-tagging, CDP, LLDP, LACP, PPag. Only display this section, in case there is switch information.  \n "
        "7 same if there is a router hooked up and router data is contained in the flows. show all connections. show gateway and subnet information. no router data, do not show anything \n"  
        "8. Conclusion: Very brief, concise summary. 3 sentences max."
    )

    user_prompt = f"Here is the telemetry data (Top 100 most relevant flows by combined Volume & Waste):\n```csv\n{csv_string}\n```\nPlease generate the full Network Intelligence Report."

    print("[+] LLM Analyzer: sending data to LLM model...")
    
    # --- last step, using API call outsourced to another module for easier management ---
    result = generate_ai_analysis(system_prompt, user_prompt)
    
    print("[+] Analysis over.")
    return result
