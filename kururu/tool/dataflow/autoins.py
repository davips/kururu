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

from akangatu.distep import DIStep
from transf.mixin.config import asConfigLess


class AutoIns(asConfigLess, DIStep):
    def _process_(self, data):
        # Forbid("inner").process(data)
        # # inner = lambda: Del("stream").process(data)  # blank stream to avoid confusion with two pointers to the same iterator
        if "stream" in data:
            print("W: field \"stream\" in data while auto inserting")
            print("HINT: you may want to blank the stream field to avoid confusion with two pointers to the same iterator.")
        return data.update(self, inner=lambda: data)
