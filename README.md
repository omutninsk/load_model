# load_model
base settings:
Index name: jaeger-*

Search object: {'query': {'constant_score': {'filter': {'bool': {'must': [{'term': {'process.serviceName': 'microservice1'}}, {'term': {'operationName': '/generate_image'}}]}}}}}

Rule	Operations	Var type	
duration	[{'name': 'copy', 'target': 'duration', 'source': '_source.duration'}]	quantitative	
x	[{'name': 'get_by_key', 'source': '_source.tags', 'target': 'endpoint', 'key': 'key', 'key_value': 'http.target', 'return_key': 'value'}, {'name': 'extract_regexp', 'source': 'endpoint', 'target': 'endpoint', 'regexp': ''}, {'name': 'copy', 'target': 'x', 'source': 'endpoint.x'}]	quantitative	
y	[{'name': 'get_by_key', 'source': '_source.tags', 'target': 'endpoint', 'key': 'key', 'key_value': 'http.target', 'return_key': 'value'}, {'name': 'extract_regexp', 'source': 'endpoint', 'target': 'endpoint', 'regexp': ''}, {'name': 'copy', 'target': 'y', 'source': 'endpoint.y'}]	quantitative	
additional	[{'name': 'get_by_key', 'source': '_source.tags', 'target': 'endpoint', 'key': 'key', 'key_value': 'http.target', 'return_key': 'value'}, {'name': 'extract_regexp', 'source': 'endpoint', 'target': 'endpoint', 'regexp': ''}, {'name': 'copy', 'target': 'additional', 'source': 'endpoint.additional'}]	categorical	
start_time	[{'name': 'copy', 'target': 'starttime', 'source': '_source.startTimeMillis'}]	quantitative