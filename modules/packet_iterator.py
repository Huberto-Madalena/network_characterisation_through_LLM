import pyshark
from typing import List, Dict, Any

def iterate_and_extract(capture: pyshark.FileCapture, target_fields: List[str]) -> List[Dict[str, Any]]:
    """
    iterate through pcap and retrieve the desired features
    """
    extracted_tuples = []
    
    for packet in capture:
        pkt_data = {'sniff_time': float(packet.sniff_timestamp)}
        
        try:
            for field in target_fields:
                val = None
                
                # 1. special case: frame.len for total PDU length
                if field == "frame.len":
                    val = packet.length
                    
                # 2. default wireshark fields
                elif '.' in field:
                    layer_name, field_name = field.split('.', 1)
                    
                    if layer_name == 'frame':
                        layer_name = 'frame_info'
                        
                    if hasattr(packet, layer_name):
                        layer = getattr(packet, layer_name)
                        pyshark_field_name = field_name.replace('.', '_')
                        val = getattr(layer, pyshark_field_name, None)
                        
                        if val is None and hasattr(layer, 'get_field_value'):
                            val = layer.get_field_value(field_name)
                
                # 3. ------------fields without a dot
                else:
                    val = getattr(packet, field, None)
                    
                # 4. cleanup for corrupted fields
                if val is not None:
                    try:
                        val = float(val)
                    except ValueError:
                        pass 
                        
                pkt_data[field] = val
                
            extracted_tuples.append(pkt_data)
        except Exception:
            continue # disregard corrupted fields
            
    capture.close()
    print(f"[+] capture reading done: {len(extracted_tuples)} relevant tuples exttracted.")
    return extracted_tuples
