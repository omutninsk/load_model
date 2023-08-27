# load_model
base settings:
Index name: jaeger-*

Search object: {'query': {'constant_score': {'filter': {'bool': {'must': [{'term': {'process.serviceName': 'microservice1'}}, {'term': {'operationName': '/generate_image'}}]}}}}}

duration	[{'name': 'copy', 'target': 'duration', 'source': '_source.duration'}]		
endpoint	[{'name': 'get_by_key', 'source': '_source.tags', 'target': 'endpoint', 'key': 'key', 'key_value': 'http.target', 'return_key': 'value'}, {'name': 'extract_regexp', 'source': 'endpoint', 'target': 'endpoint2', 'regexp': ''}]