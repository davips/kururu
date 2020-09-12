from transf.transformer import Transformer


class Split(Transformer):
    """  """

    def __init__(self, mode="cv", splits=10, test_size=0.3, seed=0, fields="X,Y", _tridxs=None, _tsidxs=None):
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
        self._trindices = _tridxs
        self._tsindices = _tsidxs
        if _tridxs is None or _tsidxs is None:
            raise NotImplementedError("Use Partition instead!")

    def _transform_(self, data):
        if data.trdata:
            raise Exception("Data already partitioned?", data)
        trmatrices, tsmatrices = {}, {}
        for f in self.fields:
            trmatrices[f] = data.field(f, self)[self._trindices]
            tsmatrices[f] = data.field(f, self)[self._tsindices]
        trdata = data.replace(**trmatrices)
        return data.replace(trdata=trdata, **tsmatrices)

    def _config_(self):
        return self._config
