import pyshark
from typing import List, Dict, Any
# import pcap iteration routine
from modules.packet_iterator import iterate_and_extract

def run_data_plane(pcap_file: str, data_plane_rules: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    settng up filter
    """
    bpf = data_plane_rules.get('bpf_filter')
    display = data_plane_rules.get('display_filter')
    target_fields = data_plane_rules.get('extract_fields', data_plane_rules.get('fields', []))
    
    # filtering logic
    final_filter_parts = []
    if bpf: final_filter_parts.append(f"({bpf})")
    if display: final_filter_parts.append(f"({display})")
    combined_filter = " and ".join(final_filter_parts) if final_filter_parts else None
    
    print(f"[+] loading {pcap_file} (combined filter: {combined_filter})")
    
    # starting up Capture
    capture = pyshark.FileCapture(
        pcap_file,
        display_filter=combined_filter,
        keep_packets=False
    )
    
    # calling outsourced logic
    return iterate_and_extract(capture, target_fields)
