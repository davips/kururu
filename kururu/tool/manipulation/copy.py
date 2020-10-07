from akangatu.distep import DIStep


class Copy(DIStep):
    def __init__(self, fromfield="Y", tofield="Z"):
        """Lazy, i.e. stream-friendly"""  # REMINDER: being lazy is needed when, e.g., chaining two or more Summs
        config = locals().copy()
        del config["self"]
        if "__class__" in config:
            del config["__class__"]
        super().__init__(config)
        self.fromfield, self.tofield = fromfield, tofield

    def _process_(self, data):
        newmatrices = {self.tofield: lambda: data.field(self.fromfield, context=self)}
        return data.replace(self, **newmatrices)
