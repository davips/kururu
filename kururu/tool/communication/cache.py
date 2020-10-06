import traceback

from akangatu.container import Container1
from tatu.amnesia import Amnesia
from tatu.persistence import Persistence
from tatu.pickle_ import Pickle
from tatu.sql.sqlite import SQLite
from transf.absdata import AbsData


class Cache(Container1):
    """Cache cannot handle stream, if any."""
    # REMINDER: com stream ele processaria em cada worker e depois o step interno tentaria processar de novo,
    # i.e. o cache criaria um stream pra competir com o oficial

    pickle = None
    sqlite = None
    amnesia = None

    def __init__(self, step, storage="sqlite", seed=0):  # TODO: what todo with seed here?
        super().__init__(step, {"seed": seed, "storage": storage})
        if storage == "pickle":
            if self.pickle is None:
                self.pickle = Pickle()
            self.storage = self.pickle
        elif storage == "sqlite":
            if self.sqlite is None:
                self.sqlite = SQLite()
            self.storage = self.sqlite
        elif storage == "amnesia":
            if self.amnesia is None:
                self.amnesia = Amnesia()
            self.storage = self.amnesia
        elif isinstance(storage, Persistence):
            self.storage = storage
        else:
            print("Unknown storage:", self.storage)
            exit()

    def _process_(self, data: AbsData):
        if data.stream:
            print(
                "Cache cannot handle stream.\nHINT: use Map(Cache(...)) or cache enclosing the expander (e.g. "
                "Partition) and Reduce.")

        hollow = data.hollow(self.step)
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
            # TODO: quando grava um frozen, é preciso marcar isso dealguma forma
            #  para que seja devidamente reconhecido como tal na hora do fetch.
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
