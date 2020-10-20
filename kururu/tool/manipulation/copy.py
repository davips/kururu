from akangatu.distep import DIStep


class Copy(DIStep):
    def __init__(self, fromfield="Y", tofield="Z"):
        """Lazy, i.e. stream-friendly"""  # REMINDER: being lazy is needed when, e.g., chaining two or more Summs
        super().__init__(fromfield=fromfield, tofield=tofield)
        self.fromfield, self.tofield = fromfield, tofield

    def _process_(self, data):
        newmatrices = {self.tofield: lambda: data.field(self.fromfield, context=self)}
        return data.update(self, **newmatrices)
