#  Copyright (c) 2020. Davi Pereira dos Santos
#  This file is part of the kururu project.
#  Please respect the license - more about this in the section (*) below.
#
#  kururu is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  kururu is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with kururu.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is a crime and is unethical regarding the effort and
#  time spent here.
#  Relevant employers or funding agencies will be notified accordingly.

from akangatu.distep import DIStep
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

    def _process_(self, data):
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
