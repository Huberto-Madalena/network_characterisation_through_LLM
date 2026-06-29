import yaml
from typing import Dict, Any, List

class RuleEngine:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.queries = self._load_rules()

    def _load_rules(self) -> List[Dict[str, Any]]:
        """loading description language from yaml file"""
        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)
                return config.get('queries', [])
        except FileNotFoundError:
            print(f"[-] configuration file {self.config_path}not found.")
            return []
        except yaml.YAMLError as exc:
            print(f"[-] error running DSL parser: {exc}")
            return []

    def get_query_plan(self, query_id: str) -> Dict[str, Any]:
        """
	search the query by ID and hand partitioning back to stream processor
        """
        for query in self.queries:
            if query.get('id') == query_id:
                print(f"[+] Query Plan created on: {query.get('id')}")
                return self._parse_query(query)
        
        raise ValueError(f"Query ID '{query_id}' in DSL not found.")

    def _parse_query(self, raw_query: Dict[str, Any]) -> Dict[str, Any]:
        """here is where abstract DSL is converted into concrete parameters."""
        plan = {
            'query_id': raw_query['id'],
            'data_plane_rules': {
                'bpf_filter': raw_query['data_plane'].get('bpf_filter'),
                'display_filter': raw_query['data_plane'].get('display_filter'),
                'fields': raw_query['data_plane'].get('extract_fields', [])
            },
            'stream_rules': raw_query.get('stream_processor', {})
        }
        return plan
