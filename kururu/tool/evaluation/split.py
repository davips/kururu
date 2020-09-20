from akangatu.dataindependent import DataIndependent


class Split(DataIndependent):
    """  """

    def __init__(self, step="train", mode="cv", splits=10, test_size=0.3, seed=0, fields="X,Y", _indices=None):
        config = locals().copy()
        del config["self"]
        del config["_tridxs"]
        del config["_tsidxs"]
        if mode == "cv":
            del config["test_size"]
        elif mode == "loo":
            del config["splts"]
            del config["test_size"]
            del config["seed"]
        elif mode == "holdout":
            pass
        else:
            raise Exception("Wrong mode: ", mode)
        self._config = config
        self.fields = fields.split(",")
        self._indices = _indices
        if _indices is None:
            raise NotImplementedError("Use Partition instead!")

    def _transform_(self, data):
        if data.inner:
            raise Exception("Data already partitioned?", data)
        newmatrices = {}
        for f in self.fields:
            newmatrices[f] = data.field(f, self)[self._indices]
        return data.replace(self, None, **newmatrices)

    def _config_(self):
        return self._config
