from functools import lru_cache

from transf.datadependent import DataDependent
from sklearn.decomposition import PCA as PCA_


class PCA(DataDependent):
    def __init__(self, *args, n=2, seed=0):
        self.n = n
        self.seed = seed
        self._config = {"n": n, "seed": seed}

    def _deptransform_(self, data, trdata):
        newtrdata = None
        if data.trdata:
            newtrX = self.model(trdata).transform(trdata.X)
            newtrdata = trdata.replace(self, trdata.uuid, X=newtrX)

        newX = self.model(trdata).transform(data.X)
        return trdata.replace(self, trdata.uuid, trdata=newtrdata, X=newX)

    def _config_(self):
        return self._config

    @lru_cache()
    def model(self, data):
        pca = PCA_(n_components=self.n, random_state=self.seed)
        pca.fit(data.X)
        return pca
