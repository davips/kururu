from akangatu.distep import DIStep


class Slice(DIStep):
    def __init__(self, first=0, last=5, fields="X,Y"):
        self._config = locals().copy()
        del self._config["self"]
        self.first, self.last = first, last
        self.fields = fields.split(",")

    def _process_(self, data):
        newfields = {k: data.field(k, self)[self.first:self.last + 1] for k in self.fields}
        return data.replace(self, **newfields)

    def _config_(self):
        pass
