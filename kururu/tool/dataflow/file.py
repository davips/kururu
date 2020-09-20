import json
from functools import cached_property

from aiuna.content.data import Data
from aiuna.content.specialdata import NoData
from aiuna.creation import read_arff
from aiuna.history import History
from akangatu.dataindependent import DataIndependent
from cruipto.uuid import UUID


class File(DataIndependent):
    def __init__(self, name, path="./", hashes=None):
        if not path.endswith("/"):
            raise Exception("Path should end with '/'", path)
        if name.endswith(".arff"):
            self._partial_config = {"name": name, "path": path}
            self.fullname = path + name
        else:
            raise Exception("Unrecognized file extension:", name)
        self._hashes = hashes

    def _transform_(self, data):
        if data is not NoData:
            raise Exception(f"Transformer {self.name} only accepts NoData. Use Sink before it if needed.")
        return self.data

    def _config_(self):
        config = self._partial_config
        config["hashes"] = self.hashes
        return config

    def _uuid_(self):  # override uuid to exclude file name/path from identity
        return UUID(json.dumps({"name": self.name, "path": self.context, "hashes": self.hashes}, sort_keys=True).encode())

    @cached_property
    def data(self):
        data_ = read_arff(self.fullname)[0]
        uuids = data_.uuids
        file_hashes = {k: v.id for k, v in uuids.items()}
        if self._hashes:
            if self._hashes != file_hashes:
                raise Exception(f"Provided hashes f{self._hashes} differs from hashes of file content: " f"{file_hashes}!")
        else:
            self._hashes = file_hashes

        return Data(uuid=UUID() * self.uuid, uuids=uuids, history=History([self]), **data_.matrices)

    @cached_property
    def hashes(self):
        if self._hashes is None:
            _ = self.data  # force calculation of hashes
        return self._hashes
