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

            if (query == b'models_list'):
                models = (postgres.NavtelecomDB.getInstance()).getModelsList()
                return (json.dumps({'status':'ok','result':models})).encode()

            if (query == b'model_add'):
                model = (postgres.NavtelecomDB.getInstance()).addModel(args[b'name'][0].decode(),int(args[b'vendor_id'][0].decode()))
                return (json.dumps({'status':'ok','result':model})).encode()

            if (query == b'model_update'):
                if(not b'vendor_id' in args):
                    model = (postgres.NavtelecomDB.getInstance()).updateModel(args[b'name'][0].decode(),int(args[b'id'][0].decode()),-1)
                else:
                    model = (postgres.NavtelecomDB.getInstance()).updateModel(args[b'name'][0].decode(), int(args[b'id'][0].decode()), int(args[b'vendor_id'][0].decode()))
                return (json.dumps({'status':'ok','result':model})).encode()

            if (query == b'model_delete'):
                model = (postgres.NavtelecomDB.getInstance()).deleteModel(int(args[b'id'][0].decode()))
                return (json.dumps({'status':'ok','result':model})).encode()

        except postgresql.exceptions.SyntaxError as ex:
            return (json.dumps({'status': 'fail', 'error':str(ex)})).encode()
        except postgresql.exceptions.ForeignKeyError as fk_ex:
            return (json.dumps({'status': 'fail', 'error': str(fk_ex)})).encode()
        #default - not found
        return (json.dumps({'status':'not_found'})).encode()