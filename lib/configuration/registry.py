import configparser

class Registry:
    _instance = None
    config = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('collector.ini')
        return

    def __del__(self):
        return

    @staticmethod
    def getInstance():
        if (Registry._instance == None):
            Registry._instance = Registry()
        return Registry._instance

    def getConfig(self):
        return self.config

    def updateConfig(self, params):
        config = configparser.RawConfigParser()
        config.add_section('default')
        config.set('default', 'default_server_port', params['default_server_port'])
        config.set('default', 'default_server_api_port', params['default_server_api_port'])

        config.add_section('threading')
        config.set('threading', 'max_threads', 32)

        config.add_section('db')
        config.set('db', 'host', params['db_host'])
        config.set('db', 'port', params['db_port'])
        config.set('db', 'db', params['db_name'])
        config.set('db', 'user', params['db_user'])
        config.set('db', 'password', params['db_password'])

        config.add_section('log')
        config.set('log', 'enable_logging', 10)
        config.set('log', 'server_log', 'collector-server.log')

        with open('collector.ini', 'w') as configfile:
            config.write(configfile)

        print("collector ini has been rewritten")
        return