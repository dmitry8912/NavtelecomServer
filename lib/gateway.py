import json
import postgresql.exceptions
from lib import postgres
from lib.registry import Registry


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

            # il_kow - Получить все устройства
            if query == b'devices_list':
                devices = (postgres.NavtelecomDB.getInstance()).getDevicesList()
                return (json.dumps({'status':'ok','result':devices})).encode()

            # il_kow - Добавить устройство
            if query == b'device_add':
                model = (postgres.NavtelecomDB.getInstance()).addModel(int(args[b'imei'][0].decode()))
                return (json.dumps({'status':'ok','result':model})).encode()

            # il_kow - Обновить устройство
            if (query == b'device_update'):
                device = (postgres.NavtelecomDB.getInstance()).updateDevice(int(args[b'imei'][0].decode()), int(args[b'ntcb_id'][0].decode()), args[b'number'][0].decode(), int(args[b'model_id'][0].decode()))
                return (json.dumps({'status':'ok', 'result':device})).encode()

            # il_kow - Добавить устройство (postgres функция device_new)
            if query == b'device_new':
                device = (postgres.NavtelecomDB.getInstance()).newDevice(int(args[b'imei'][0].decode()), int(args[b'model_id'][0].decode()))
                return (json.dumps({'status':'ok', 'result':device})).encode()

            # il_kow - Удалить утсройство
            if query == b'device_delete':
                device = (postgres.NavtelecomDB.getInstance()).deleteDevice(int(args[b'imei'][0].decode()))
                return (json.dumps({'status':'ok', 'result':device})).encode()

            # il_kow - Получить все модели по id производителя
            if query == b'get_vendor_models':
                models = (postgres.NavtelecomDB.getInstance()).getModelsListByVendor(int(args[b'vendor_id'][0].decode()))
                return (json.dumps({'status': 'ok', 'result': models})).encode()


            # il_kow - Получить все настройки (файл collector.ini)
            if query == b'get_settings':
                collector_ini = Registry.getInstance().getConfig()
                settings = {
                    'default_server_port' : collector_ini['default']['default_server_port'],
                    'default_server_api_port' : collector_ini['default']['default_server_api_port'],
                    'db_host' : collector_ini['db']['host'],
                    'db_port' : collector_ini['db']['port'],
                    'db_name' : collector_ini['db']['db'],
                    'db_user' : collector_ini['db']['user'],
                    'db_password': collector_ini['db']['password']
                }
                return (json.dumps({'status': 'ok', 'result':settings})).encode()

            # il_kow - Сохранить настройки (файл collector.ini)
            if query == b'set_settings':
                registry = Registry()
                settings = {
                    'default_server_port' : args[b'default_server_port'][0].decode(),
                    'default_server_api_port' : args[b'default_server_api_port'][0].decode(),
                    'db_host' : args[b'db_host'][0].decode(),
                    'db_port' : args[b'db_port'][0].decode(),
                    'db_name' : args[b'db_name'][0].decode(),
                    'db_user' : args[b'db_user'][0].decode(),
                    'db_password' : args[b'db_password'][0].decode(),
                }
                registry.updateConfig(settings)

            # il_kow - Получить все приемники
            if query == b'receivers_list':
                receivers = (postgres.NavtelecomDB.getInstance()).getReceiversList()
                return (json.dumps({'status': 'ok', 'result': receivers})).encode()

            # il_kow - Добавить приемник
            if query == b'receiver_add':
                receiver = (postgres.NavtelecomDB.getInstance()).addReceiver(args[b'name'][0].decode(),
                                                                            args[b'address'][0].decode(),
                                                                            args[b'port'][0].decode())
                return (json.dumps({'status': 'ok', 'result': receiver})).encode()

            # il_kow - Редактировать приемник
            if query == b'receiver_update':
                receiver = (postgres.NavtelecomDB.getInstance()).updateReceiver(int(args[b'id'][0].decode()),
                                                                                args[b'name'][0].decode(),
                                                                                args[b'address'][0].decode(),
                                                                                args[b'port'][0].decode())
                return (json.dumps({'status': 'ok', 'result': 'success'})).encode()

        except postgresql.exceptions.SyntaxError as ex:
            return (json.dumps({'status': 'fail', 'error':str(ex)})).encode()
        except postgresql.exceptions.ForeignKeyError as fk_ex:
            return (json.dumps({'status': 'fail', 'error': str(fk_ex)})).encode()
        # default - not found
        return (json.dumps({'status':'not_found'})).encode()