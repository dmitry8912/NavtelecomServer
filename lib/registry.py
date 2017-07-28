import configparser

class Registry:
    _instance = None
    config = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('../collector.ini')
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