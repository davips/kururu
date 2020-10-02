from akangatu.distep import DIStep
from transf.absdata import AbsData


# TODO: create Numpy step:  Numpy(method="sort", fromfield="A", tofield="B")
class Sort(DIStep):
    """Sort all provided matrices by a column(or row) of the first one."""

    def __init__(self, fields="U,X", byindex=0, along="rows"):
        super().__init__({"fields": fields, "index": byindex, "by": along})
        self.fields = fields.split(",")
        self.along = along
        self.byindex = byindex
        if along not in ["rows", "cols"]:
            print(self.name, f"Unknown type of entry to rank: by='{along}'. Should be 'rows' or 'cols'.")
            exit()

    def _process_(self, data: AbsData):
        M = data.field(self.fields[0], context=self)
        if self.along == "rows":
            indices = M[:, self.byindex].argsort()
        else:
            indices = M[self.byindex, :].argsort()

        dic = {}
        for field in self.fields:
            M = data.field(field, context=self)
            if self.along == "rows":
                dic[field] = M[indices, :]
            else:
                dic[field] = M[:, indices]

        return data.replace(self, **dic)
