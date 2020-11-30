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
#

from imblearn.under_sampling import RandomUnderSampler as imbRUS

from akangatu.abs.mixin.macro import asMacro
from akangatu.operator.unary.inop import In
from kururu.tool.enhancement.instance.sampling.abs.sampler import Sampler


class RUS_(Sampler):
    """Reduce the occurrence of all classes so as to be equal to the amount of instances in the minority class
    (default behavior)."""

    def __init__(self, strategy='not minority', replacement=False, seed=0):
        super().__init__(strategy=strategy, replacement=replacement, seed=seed)
        self.strategy = strategy
        self.replacement = replacement
        self.seed = seed

    def _algorithm_func(self):
        return lambda: imbRUS(sampling_strategy=self.strategy, replacement=self.replacement, random_state=self.seed)


class RUS(asMacro, RUS_):
    """Apply random under sampling to process inner data instead of using the outer data."""
    def _step_(self):
        return In(RUS_(**self.held))
