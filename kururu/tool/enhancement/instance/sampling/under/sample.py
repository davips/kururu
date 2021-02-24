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
from sklearn.utils import resample

from akangatu.abs.mixin.macro import asMacro
from akangatu.operator.unary.inop import In
from kururu.tool.enhancement.instance.sampling.abs.sampler import Sampler


class Sample_(Sampler):
    """Reduce the occurrence of all classes proportionally (or not)."""

    def __init__(self, n=100, replace=False, seed=0, ignore_badarg=False):
        super().__init__(n=n, replace=replace, seed=seed, ignore_badarg=ignore_badarg)
        self.n = n
        self.replace = replace
        self.seed = seed
        self.ignore_badarg = ignore_badarg

    def _algorithm_func(self):
        def f(X, y):
            n = min(self.n, X.shape[0]) if self.ignore_badarg else self.n
            return resample(X, y, n_samples=n, stratify=y, replace=self.replace, random_state=self.seed)

        return lambda: f


class Sample(asMacro, Sample_):
    """Apply sampling to process inner data instead of using the outer data."""

    def _step_(self):
        return In(Sample_(**self.held))
