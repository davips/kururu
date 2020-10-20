from scipy.stats import rankdata
from transf.absdata import AbsData

from akangatu.distep import DIStep


class Rank(DIStep):
    """Rank all columns(or rows) independently, or by a given column/row that must exist in all matrices."""

    def __init__(self, fields="U", byindex=0, along="rows"):
        super().__init__(fields=fields, byindex=byindex, along=along)
        self.fields = fields.split(",")
        self.along = along
        self.byindex = byindex
        if along not in ["rows", "cols"]:
            print(self.name, f"Unknown type of entry to rank: by='{along}'. Should be 'rows' or 'cols'.")
            exit()

    def _process_(self, data: AbsData):
        dic = {}
        for field in self.fields:
            def result():
                M = data[field]
                if self.byindex is not None:
                    M = M[:, self.byindex] if self.along == "rows" else M[self.byindex, :]
                if self.along == "rows":
                    return (rankdata(M, axis=0) - 1).astype(int)
                return (rankdata(M, axis=1) - 1).astype(int)

            dic["r" + field] = result
        return data.update(self, **dic)
