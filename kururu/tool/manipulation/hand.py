from akangatu.distep import DIStep
class Hand(DIStep):
    """Ask the user for a value."""

    def __init__(self, field="Q"):
        super().__init__(field=field)

    def _process_(self, data):
        dic = {self.field: value}
        return data.update(self, **dic)
