from functools import lru_cache

from sklearn.model_selection import StratifiedShuffleSplit, StratifiedKFold, LeaveOneOut

from cururu.tool.evaluation.split import Split
from cururu.base.dataindependent import DataIndependent


class Partition(DataIndependent):
    def __init__(self, mode="cv", splits=10, test_size=0.3, seed=0, fields="X,Y"):
        config = locals().copy()
        del config["self"]
        if mode == "cv":
            del config["test_size"]
            self.algorithm = StratifiedKFold(shuffle=True, n_splits=splits, random_state=seed)
        elif mode == "loo":
            del config["tests"]
            del config["test_size"]
            del config["seed"]
            self.algorithm = LeaveOneOut()
        elif mode == "holdout":
            self.algorithm = StratifiedShuffleSplit(n_splits=splits, test_size=test_size, random_state=seed)
        else:
            raise Exception("Wrong mode: ", mode)
        self._config = config
        self.splits = splits

    def _transform_(self, data):
        """"""
        idxs = self.partitionings(data)
        for i in range(self.splits):
            s = Split(**self.config, _tridxs=idxs[i][0], _tsidxs=idxs[i][1])
            raise NotImplemented

    def _config_(self):
        return self._config

    @lru_cache()
    def partitionings(self, data):
        X, y = data.Xy  # TODO: add other scenarios beyond classification?
        return list(self.algorithm.split(X=X, y=y))
