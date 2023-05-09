from elasticsearch import Elasticsearch

class ES_Connector():
    es = None
    host = None
    port = None


    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        try:
            self._connect_elasticsearch()
        except Exception as e:
            print(str(e))
            raise
    
    def _connect_elasticsearch(self):
        self.es = Elasticsearch([{'host': self.host, 'port': self.port}])
        if self.es.ping():
            print('connection ok')
        else:
            print('connection fail')

    def get_indexes_list(self):
        return self.es.indices.get_alias("*")

    def search(self, index_name, search, count):
        return self.es.search(index=index_name, body=search, size=count)
    
    # def count(self, index_name, search, n):
    #     return self.es.count(index=index_name, body=search)[100]