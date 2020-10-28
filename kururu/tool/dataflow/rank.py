#  Copyright (c) 2020. Davi Pereira dos Santos
#      This file is part of the kururu project.
#      Please respect the license. Removing authorship by any means
#      (by code make up or closing the sources) or ignoring property rights
#      is a crime and is unethical regarding the effort and time spent here.
#      Relevant employers or funding agencies will be notified accordingly.
#
#      kururu is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      kururu is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with kururu.  If not, see <http://www.gnu.org/licenses/>.
#

from scipy.stats import rankdata
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

    def _process_(self, data):
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
