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

from sklearn.decomposition import PCA as PCAsk

from aiuna.step.delete import Del
from akangatu.abs.mixin.macro import asMacro
from akangatu.operator.unary.inop import In
from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.enhancement.attribute.abs.transformer import Transformer
from akangatu.transf.config import globalcache


class PCAo(Transformer):
    """Reduce dimensionality by PCA. Use inner data as "training" data, but transform only the outer data.

    Hint: use PCA to transform both inner and outer data."""

    def __init__(self, inner=None, n=2, seed=0):
        self.n = n
        self.seed = seed
        super().__init__(inner, n=n, seed=seed)

    def translate(self, exception, data):
        msg = str(exception)
        if "n_components=" in msg and "must be between 0 and min(n_samples, n_features)=" in msg:
            return f"n:{self.n} > Xw{data.Xw} or n:{self.n} > Xh{data.Xh}"

    def _algorithm_func(self):
        return lambda: PCAsk(n_components=self.n, random_state=self.seed)


class PCAb(asMacro, PCAo):
    """Apply PCA to transform both inner and outer data. Inner data is used as "training" data."""

    def _step_(self):
        pca = PCAo(**self.held)
        return pca * In(AutoIns * pca * Del("inner"))


pca = PCAb()


# l = []
# for i in range(1, 28):
#     l.append(round(pow(1.2, i)))
# print(sorted(list(set(l))))
