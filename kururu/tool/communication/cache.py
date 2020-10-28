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
from tatu.amnesia import Amnesia
from tatu.storage import Storage
from tatu.pickle_ import Pickle
from tatu.sql.sqlite import SQLite


class Cache(Container1):
    """Cache cannot handle stream, if any.

    Cache triggers strictness on fields when self.step.process() needs to be called
    (but not when they just come from storage, which would activate the other type of lazyness, the storage one)."""
    # REMINDER: com stream ele processaria em cada worker e depois o step interno tentaria processar de novo,
    # i.e. o cache criaria um stream pra competir com o oficial
    # Pra ficar mais claro: o cache precisa *conter*
    # NOVA solução: o cache não pode prever o resultado do worker no stream (ou pode?),
    # mas pode prever o uuid resultante e assim ter o que colocar num field streamed e pode enxertar mini caches sobre cada worker;
    #  No Accumulator().end_func() pode storar o data contenedor propriamente
    # Assim, stream poderia ser outro campo string por virgulas no SQL.
    # Pra facilitar, os streamers poderiam fornecer um meio de enxertar conteiner neles.

    storages = {}

    def __init__(self, step, storage="sqlite", seed=0):  # TODO: what todo with seed here?
        super().__init__(step, seed=seed, storage=storage)
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
    ???? ver se vai haver cache container. o único motivo seria caso a montagem dos campos lazy tenha muito overhead
    # def _process_(self, data: Data):
    #     # TODO ver no papel como fazer mini Caches p/ stream (se é versdade)
    #     planned = data >> self.step
    #     fetched = self.storage.lazyfetch(planned, lock=True)
    #     if fetched:
    #         return fetched
    #     return self.storage.lazystore(planned)

    # TODO dar unlock() no data.getitem se exception

    def _uuid_(self):
        return self.step.uuid
