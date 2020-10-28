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

# Creating a custom step
from akangatu.distep import DIStep


# DIStep means "Data Independent Step", i.e. it does not depend on previously known data.
class MyAdditionStep(DIStep):
    """Multiplies the given field by a factor."""

    def __init__(self, field, factor):
        # All relevant step parameters should be passed to super() as keyword arguments.
        super().__init__(field=field, factor=factor)

        # Instance attributes are set as usual.
        self.field = field
        self.factor = factor

    def _process_(self, data):
        # All calculations (including access to data fields)
        #   is deferred to a future access to the return field - R in this case.
        return data.update(self, R=lambda: data[self.field] * self.factor)
