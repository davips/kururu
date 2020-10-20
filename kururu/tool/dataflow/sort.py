from akangatu.distep import DIStep
from transf.absdata import AbsData


# TODO: create Numpy step:  Numpy(method="sort", fromfield="A", tofield="B")
class Sort(DIStep):
    """Sort all provided matrices by a column(or row) of the first one."""

    def __init__(self, fields="U,X", byindex=0, reverse=False, along="rows"):
        super().__init__(fields=fields, byindex=byindex, reverse=reverse, along=along)
        self.fields = fields.split(",")
        self.along = along
        self.byindex = byindex
        self.reverse = reverse
        if along not in ["rows", "cols"]:
            print(self.name, f"Unknown type of entry to sort: by='{along}'. Should be 'rows' or 'cols'.")
            exit()  # TODO: generalize these checkings/errors

    def _process_(self, data: AbsData):
        M = data.field(self.fields[0], context=self)
        if self.along == "rows":
            indices = M[:, self.byindex].argsort()
        else:
            indices = M[self.byindex, :].argsort()

        if self.reverse:
            indices = indices[::-1]

        dic = {}
        for field in self.fields:
            M = data.field(field, context=self)
            if self.along == "rows":
                dic[field] = M[indices, :]
            else:
                dic[field] = M[:, indices]

        return data.update(self, **dic)


class Sortr(Sort):
    """Shortcut for Sort(..., reverse=True)"""
    def __init__(self, fields="U,X", byindex=0, along="rows"):
        super().__init__(fields, byindex, True, along)
