from twisted.web import server, resource
from twisted.internet import reactor

class Simple(resource.Resource):
    isLeaf = True

    def __init__(self, server):
        self.server = server
        return
    def render_GET(self,request):
        return self.server.getCurrentStateInfo()