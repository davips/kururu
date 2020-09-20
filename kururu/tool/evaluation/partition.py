from functools import lru_cache

from sklearn.model_selection import StratifiedShuffleSplit, StratifiedKFold, LeaveOneOut

from kururu.tool.evaluation.split import Split
from akangatu.dataindependent import DataIndependent


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
        # REMINDER: Partition faz data virar data com stream; e nesse stream vem data transformado e com inner.
        for i in range(self.splits):
            trainS = Split(**self.config, _indices=idxs[i][0])
            testS = Split(**self.config, _indices=idxs[i][1])


    def _config_(self):
        return self._config

    @lru_cache()
    def partitionings(self, data):
        X, y = data.Xy  # TODO: add other scenarios beyond classification?
        return list(self.algorithm.split(X=X, y=y))
