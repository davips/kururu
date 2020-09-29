from akangatu.distep import DIStep


class Slice(DIStep):
    def __init__(self, first=0, last=5, fields="X,Y"):
        config = locals().copy()
        del config["self"]
        super().__init__(config)  # REMINDER: super call after locals should be before references to self, to avoid "__class__" in the dict (? not sure about that)
        self.first, self.last = first, last
        self.fields = fields.split(",")

    def _process_(self, data):
        newfields = {k: data.field(k, context=self)[self.first:self.last + 1] for k in self.fields}
        return data.replace(self, **newfields)
