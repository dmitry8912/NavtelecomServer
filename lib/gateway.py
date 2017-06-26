import json
import postgresql.exceptions
from lib import postgres

class Gateway:
    _instance = None

    def __init__(self):
        return

    def __del__(self):
        return

    @staticmethod
    def executeQuery(query,args):
        try:
            # vendors list
            if (query == b'vendors_list'):
                vendorsList  = (postgres.NavtelecomDB.getInstance()).getVendorsList()
                return (json.dumps({'status':'ok','result':vendorsList})).encode()

            #adding a vendor by name
            if (query == b'vendor_add'):
                vendorAdd = (postgres.NavtelecomDB.getInstance()).addVendor(args[b'name'][0].decode())
                return (json.dumps({'status':'ok','result':vendorAdd})).encode()

            if (query == b'vendor_update'):
                vendor = (postgres.NavtelecomDB.getInstance()).updateVendor(int(args[b'id'][0].decode()),args[b'name'][0].decode())
                return (json.dumps({'status':'ok','result':vendor})).encode()

            if (query == b'vendor_delete'):
                vendor = (postgres.NavtelecomDB.getInstance()).deleteVendor(int(args[b'id'][0].decode()))
                return (json.dumps({'status':'ok','result':vendor})).encode()

        except postgresql.exceptions.SyntaxError as ex:
            return (json.dumps({'status': 'fail', 'error':str(ex)})).encode()
        #default - not found
        return (json.dumps({'status':'not_found'})).encode()