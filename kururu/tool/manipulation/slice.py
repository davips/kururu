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


class Slice(DIStep):
    """Select rows(or columns) inside a given interval, including limits."""

    def __init__(self, code=":5", fields="X,Y"):
        # REMINDER: super call with locals leads to infinite loop
        super().__init__(code=code, fields=fields)

        # https://stackoverflow.com/a/51105983/9681577
        def toslice(txt):
            return slice(*map(lambda x: int(x.strip()) if x.strip() else None, txt.split(':')))

        self.slice = [toslice(txt) for txt in code.split(",")]
        self.fields = fields.split(",")

    def _process_(self, data):
        newfields = {k: (lambda k_: lambda: data[k_][self.slice])(k) for k in self.fields}
        return data.update(self, **newfields)
