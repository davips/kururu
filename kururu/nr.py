from akangatu.distep import DIStep
from transf.absdata import AbsData


class NR(DIStep):
    def __init__(self, n=5):
        self._config = {"n": n}

    def _process_(self, data: AbsData):
        newX = ...
        data...
        return data.replace(self, X=newX)

    def _config_(self):
        return self._config
