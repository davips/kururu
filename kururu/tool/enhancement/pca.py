from transf.config import globalcache
from aiuna.content.data import Data
from akangatu.abs.mixin.macro import asMacro
from akangatu.ddstep import DDStep
from akangatu.operator.unary.inop import In
from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.dataflow.delin import DelIn
from sklearn.decomposition import PCA as PCA_


class PCA1(DDStep):
    def __init__(self, inner=None, n=2, seed=0):
        self.n = n
        self.seed = seed
        super().__init__(inner, n=n, seed=seed)

    def _process_(self, data: Data):
        newX = self.model(data.inner).transform(data.X)
        return data.update(self, X=newX)

    def translate(self, exception, data):
        msg = str(exception)
        if "n_components=" in msg and "must be between 0 and min(n_samples, n_features)=" in msg:
            return f"n:{self.n} > Xw{data.Xw} or n:{self.n} > Xh{data.Xh}"

    @globalcache
    def model(self, data):
        pca = PCA_(n_components=self.n, random_state=self.seed)
        pca.fit(data.X)
        return pca


class PCA(asMacro, PCA1):
    def _step_(self):
        pca = PCA1(**self.held)
        return pca * In(AutoIns * pca * DelIn)

# l = []
# for i in range(1, 28):
#     l.append(round(pow(1.2, i)))
# print(sorted(list(set(l))))
