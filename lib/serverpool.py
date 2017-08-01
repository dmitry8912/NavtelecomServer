from multiprocessing import Process, Manager, SimpleQueue
import os
from lib.navtelecom import *
from lib.postgres import NavtelecomDB

class ServerPool:
    _instance = None
    _manager = None
    server_pool = []

    @staticmethod
    def getInstance():
        if ServerPool._instance == None:
            ServerPool._instance = ServerPool()
        return ServerPool._instance

    @staticmethod
    def doJob(data, imei):
        navtel = Navtelecom()
        decodedBytes = navtel.decodeSinglePacket(data)
        db = NavtelecomDB.getInstance()
        db.addDecodedPacket(imei, str(decodedBytes))

        print(str(data) + ' => ' + str(os.getpid()) + ' job done')
        return

    def addProcess(self, data, imei):
        print("JOB_HAS_BEEN_STARTED")
        for p in self.server_pool:  # Убивание экземпляров класса Process
            if not p.is_alive():
                self.server_pool.remove(p)
        print(str(len(self.server_pool))+' processes in queue')
        if len(self.server_pool) > 25:  # Количество одновременных потоков
            return
        p = Process(target=ServerPool.doJob, args=(data, imei))
        self.server_pool.append(p)
        p.start()
        return
