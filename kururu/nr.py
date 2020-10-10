from akangatu.distep import DIStep
from transf.absdata import AbsData


class NR(DIStep):
    def __init__(self, n=5):
        super().__init__({"n": n})

    def _process_(self, data: AbsData):
        # newX = ...
        # data...
        # return data.update(self, X=newX)
        pass
