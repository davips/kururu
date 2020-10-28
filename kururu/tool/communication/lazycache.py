#  Copyright (c) 2020. Davi Pereira dos Santos
#      This file is part of the kururu project.
#      Please respect the license. Removing authorship by any means
#      (by code make up or closing the sources) or ignoring property rights
#      is a crime and is unethical regarding the effort and time spent here.
#      Relevant employers or funding agencies will be notified accordingly.
#
#      kururu is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      kururu is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with kururu.  If not, see <http://www.gnu.org/licenses/>.
#

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
