from functools import lru_cache

from sklearn.decomposition import PCA as PCA_

from akangatu.datadependent import DataDependent


class PCA(DataDependent):
    def __init__(self, *args, n=2, seed=0):
        self.n = n
        self.seed = seed
        self._config = {"n": n, "seed": seed}

    def _transform_(self, data):
        newX = self.model(data.inner).transform(data.X)
        return data.replace(self, X=newX)

    def _config_(self):
        return self._config

    @lru_cache()
    def model(self, data):
        pca = PCA_(n_components=self.n, random_state=self.seed)
        pca.fit(data.X)
        return pca


# l = []
# for i in range(1, 128):
#     l.append(round(pow(1.05, i)))
# print(sorted(list(set(l))))
