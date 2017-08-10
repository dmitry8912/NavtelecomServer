from twisted.web import resource

from lib.database.gateway import Gateway as gw


class Simple(resource.Resource):
    isLeaf = True

    def __init__(self, server):
        self.server = server
        return
    def render_GET(self,request):
        request.setHeader('Access-Control-Allow-Origin','*')
        request.setHeader('Access-Control-Max-Age', '1000')
        request.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Content-Type, Origin, Authorization, Accept, Client-Security-Token, Accept-Encoding')
        request.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE, PUT')
        if(len(request.postpath) == 1 and request.postpath[0] == b''):
            return self.server.getCurrentStateInfo()
        else:
            return gw.executeQuery(request.postpath[0], request.args)

    def render_POST(self,request):
        if (len(request.postpath) == 0):
            return self.server.getCurrentStateInfo()
        else:
            return gw.executeQuery(request.postpath[0], request.args)