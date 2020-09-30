import traceback

from akangatu.container import Container1
from tatu.okaserver import OkaServer
from tatu.pickleserver import PickleServer
from tatu.storage import Storage
from transf.absdata import AbsData


class Cache(Container1):
    def __init__(self, step, storage_alias="default_dump", seed=0):
        super().__init__(step, {"seed": seed, "storage_alias": storage_alias})
        self.storage = Storage(storage_alias)
        # self.storage = PickleServer()
        # self.storage = OkaServer(post=True, token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDE0NjIzMTgsIm5iZiI6MTYwMTQ2MjMxOCwianRpIjoiYzIwMGUzZmItZjBhZC00MjFjLWJmZGYtNDE2YWUzNDA4YmRjIiwiZXhwIjoxNjAyNzU4MzE4LCJpZGVudGl0eSI6ImRhdmlwcyIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.IHQo2TNHVlDuTCrAppO93RESeqSX1MCBeVlHBCFG_80")

    def _process_(self, data: AbsData):
        hollow = data.hollow(self.step)
        output_data = self.storage.fetch(hollow, lock=True)

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

        return output_data
