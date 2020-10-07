from sklearn.model_selection import StratifiedKFold, LeaveOneOut, StratifiedShuffleSplit

from transf.config import globalcache


class withPartitioning:
    def __init__(self, mode, config):
        if mode == "cv":
            del config["test_size"]
            self.algorithm = StratifiedKFold(shuffle=True, n_splits=config["splits"], random_state=config["seed"])
        elif mode == "loo":
            del config["tests"]
            del config["test_size"]
            del config["seed"]
            self.algorithm = LeaveOneOut()
        elif mode == "holdout":
            self.algorithm = StratifiedShuffleSplit(n_splits=config["splits"], test_size=config["test_size"], random_state=config["seed"])
        else:
            raise Exception("Wrong mode: ", mode)
        self._config = config
        self.splits = config["splits"]
        self.fields = config["fields"].split(",")

    @globalcache
    def partitionings(self, data):
        X, y = data.Xy  # TODO: add other scenarios beyond classification?
        return list(self.algorithm.split(X=X, y=y))

    def _config_(self):
        return self._config
