import numpy as np
from akangatu.distep import DIStep


class Slice(DIStep):
    """Select rows(or columns) inside a given interval, including limits."""
    def __init__(self, first=0, last=5, fields="X,Y"):
        super().__init__({"first": first, "last": last, "fields": fields})  # REMINDER: super call with locals lead to infinite loop
        self.first, self.last = first, last
        self.fields = fields.split(",")

    def _process_(self, data):
        first = self.first
        last = self.last
        if first < 0:
            if last >= 0:
                print("First cannot be negative while last is non negative:", first, last)
            first -= 1
            last -= 1

        if first == last:
            newfields = {k: data.field(k, context=self)[first].reshape(1, -1) for k in self.fields}
        else:
            newfields = {k: data.field(k, context=self)[first:last + 1] for k in self.fields}
        return data.replace(self, **newfields)
