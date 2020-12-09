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

from imblearn.over_sampling import RandomOverSampler as imbROS

from akangatu.abs.mixin.macro import asMacro
from akangatu.ddstep import DDStep
from akangatu.operator.unary.inop import In
from kururu.tool.enhancement.instance.sampling.abs.sampler import Sampler


class ROS_(Sampler):
    """Increase number of instances of all classes so as to be equal to the amount of instances in the majority class
    (default behavior)."""

    def __init__(self, strategy="not majority", seed=0):
        super().__init__(strategy=strategy, seed=seed)
        self.strategy = strategy
        self.seed = seed

    def _algorithm_func(self):
        return lambda: imbROS(sampling_strategy=self.strategy, random_state=self.seed)


# class ROS(DDStep):
#     """Apply random over sampling to process inner data instead of using the outer data."""
#
#     def __init__(self, inner=None, strategy="not majority", seed=0):
#         DDStep.__init__(self, inner, strategy=strategy, seed=seed)
#         self.strategy = strategy
#         self.seed = seed
#
#     def _process_(self, data):
#         d = data >> In(ROS_(**self.held))
#         return data.update(self, **{k: d.field_funcs_m[k] for k in d.changed})
#
class ROS(asMacro, DDStep):
    """Apply random over sampling to process inner data instead of using the outer data."""
    def __init__(self, inner=None, strategy="not majority", seed=0):
        DDStep.__init__(self, inner, strategy=strategy, seed=seed)
        self.strategy = strategy
        self.seed = seed

    def _step_(self):
        return In(ROS_(**self.held))
