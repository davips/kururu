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


class Copy(DIStep):
    def __init__(self, fromfield="Y", tofield="Z"):
        """Lazy, i.e. stream-friendly"""  # REMINDER: being lazy is needed when, e.g., chaining two or more Summs
        super().__init__(fromfield=fromfield, tofield=tofield)
        self.fromfield, self.tofield = fromfield, tofield

    def _process_(self, data):
        newmatrices = {self.tofield: lambda: data.field(self.fromfield, context=self)}
        return data.update(self, **newmatrices)
