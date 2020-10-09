from akangatu.distep import DIStep
from transf.absdata import AbsData


class Hand(DIStep):
    """Ask the user for a value."""

    def __init__(self, field="Q"):
        super().__init__({"field": field})

    def _process_(self, data: AbsData):
        dic = {self.field: value}
        return data.replace(self, **dic)
