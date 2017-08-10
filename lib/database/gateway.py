import json

import postgresql.exceptions

from lib.configuration.registry import Registry


class Gateway:
    _instance = None

    def __init__(self):
        return

    def __del__(self):
        return

    @staticmethod
    def executeQuery(query,args):
        try:
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

        except postgresql.exceptions.SyntaxError as ex:
            return (json.dumps({'status': 'fail', 'error':str(ex)})).encode()
        except postgresql.exceptions.ForeignKeyError as fk_ex:
            return (json.dumps({'status': 'fail', 'error': str(fk_ex)})).encode()
        # default - not found
        return (json.dumps({'status':'not_found'})).encode()