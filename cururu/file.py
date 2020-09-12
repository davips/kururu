import json
from functools import cached_property

from pjdata.aux.uuid import UUID
from pjdata.content.data import Data
from pjdata.content.specialdata import NoData
from pjdata.creation import read_arff
from pjdata.history import History
from transf.transformer import Transformer


class File(Transformer):
    def __init__(self, name, path="./", hashes=None, **kwargs):
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
        return UUID(json.dumps(self.hashes).encode())

    @cached_property
    def data(self):
        file_hashes, data_, _, _, uuids = read_arff(self.fullname)
        if self._hashes:
            if self._hashes != file_hashes:
                raise Exception(f"Provided hashes f{self._hashes} differs from hashes of file content: " f"{file_hashes}!")
        else:
            self._hashes = file_hashes

        return Data(
            history=History([self]),
            failure=None,
            frozen=False,
            hollow=False,
            stream=None,
            storage_info=None,
            uuid=UUID() * self.uuid,
            uuids=uuids,
            **data_.matrices
        )

    @cached_property
    def hashes(self):
        if self._hashes is None:
            _ = self.data  # force calculation of hashes
        return self._hashes
