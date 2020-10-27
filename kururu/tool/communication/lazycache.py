import traceback

from aiuna.content.data import Data
from akangatu.container import Container1
from akangatu.distep import DIStep
from tatu.amnesia import Amnesia
from tatu.storage import Storage
from tatu.pickle_ import Pickle
from tatu.sql.sqlite import SQLite
from transf.mixin.noop import asNoOp


class LCache(asNoOp, DIStep):
    storages = {}

    def __init__(self, storage="sqlite", eager_store=True, seed=0):  # TODO: what todo with seed here?
        super().__init__(storage=storage, eager_store=eager_store, seed=seed)
        if storage == "pickle":
            storage = Pickle()
        elif storage == "sqlite":
            storage = SQLite()
        elif storage == "amnesia":
            storage = Amnesia()
        elif not isinstance(storage, Storage):
            print("Unknown storage:", self.storage)
            exit()
        if storage.id not in self.storages:
            self.storages[storage.id] = storage
        self.storage = self.storages[storage.id]
        self.eager_store=eager_store


    def _process_(self, data: Data):
        global c
        print("bef fetch")
        if c > 0:
            raise Exception()
        c += 1
        fetched = self.storage.fetch(data, lock=True,lazy=False)
        print("aft fetch")
        if fetched:
            return fetched
        print("bef store")
        ret = self.storage.store(data, unlock=True, lazy=not self.eager_store)
        print("aft store")
        return ret

    # TODO dar unlock() no data.getitem se exception

c = 0
