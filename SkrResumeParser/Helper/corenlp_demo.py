import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from pprint import pprint

'''
run first corenlp python script from stanford folder and then run this file
Dependency Parser
'''

class StanfordNLP:
    def __init__(self):
        self.server = ServerProxy(JsonRpc20(),
                                  TransportTcpIp(addr=("127.0.0.1", 8080)))

    def parse(self, text):
        return json.loads(self.server.parse(text))


nlp = StanfordNLP()
data = '''the teacher eats a red apple'''
result = nlp.parse(data)
pprint(result)
