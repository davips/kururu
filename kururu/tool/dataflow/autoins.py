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
from akangatu.transf.mixin.config import asConfigLess


class AutoIns(asConfigLess, DIStep):
    """Insert a data as the inner of itself."""
    def _process_(self, data):
        # Forbid("inner").process(data)
        # # inner = lambda: Del("stream").process(data)  # blank stream to avoid confusion with two pointers to the same iterator
        if "stream" in data:
            print("W: field \"stream\" in data while auto inserting")
            print("HINT: you may want to blank the stream field to avoid confusion with two pointers to the same iterator.")
        return data.update(self, inner=lambda: data)
