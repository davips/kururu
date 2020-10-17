import traceback

from akangatu.container import Container1
from tatu.amnesia import Amnesia
from tatu.storage import Storage
from tatu.pickle_ import Pickle
from tatu.sql.sqlite import SQLite
from transf.absdata import AbsData


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
        super().__init__(step, {"seed": seed, "storage": storage})
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

    def _process_(self, data: AbsData):
        if data.stream:
            # TODO ver papel e repensar essa restrição
            print("Cache cannot handle stream.\nHINT: use Map(Cache(...)) or cache enclosing both the expander (e.g. Partition) and Reduce.")

        hollow = self.step << data
        output_data = self.storage.fetch(hollow, lock=True)  # TODO: restore inner

        # Process if still needed  ----------------------------------
        if output_data is None:
            try:
                # REMINDER: exit_on_error=False is to allow storage to cleanup after an error
                output_data = self.step.process(data, exit_on_error=False)
            except:
                self.storage.unlock(hollow)
                traceback.print_exc()
                exit(0)
            # TODO: confirmar que failure/timeout/? são gravados e recuperados
            self.storage.store(output_data, check_dup=False)

        # print(data.id)
        # print(hollow.id)
        # print(output_data.id)
        # print("..................")
        # print(data.inner.id)
        # print(hollow.inner.id)
        # print(output_data.inner.id)
        # print('------------------------')
        return output_data

    def _uuid_(self):
        return self.step.uuid
