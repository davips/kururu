from sklearn.decomposition import PCA as PCA_

from aiuna.config import globalcache
from aiuna.content.data import Data
from akangatu.datadependent import DataDependent
from akangatu.abs.mixin.macro import asMacro
from akangatu.operator.unary.inop import In
from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.dataflow.delin import DelIn


class PCA1(DataDependent):
    def __init__(self, n=2, seed=0):
        self.n = n
        self.seed = seed
        self._config = {"n": n, "seed": seed}

    def _transform_(self, data: Data):
        newX = self.model(data.inner).transform(data.X)
        return data.replace(self, X=newX)

    def _config_(self):
        return self._config

    @globalcache
    def model(self, data):
        pca = PCA_(n_components=self.n, random_state=self.seed)
        pca.fit(data.X)
        return pca


class PCA(asMacro, PCA1):
    def _transformer_(self):
        return PCA1(**self.held) * In(AutoIns * PCA1(**self.held) * DelIn)

# l = []
# for i in range(1, 128):
#     l.append(round(pow(1.05, i)))
# print(sorted(list(set(l))))
