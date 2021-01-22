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

from abc import ABC, abstractmethod

from akangatu.transf.config import globalcache
from aiuna.content.data import Data
from akangatu.ddstep import DDStep


class Predictor(DDStep, ABC):
    """  """

    def _process_(self, data: Data):
        matrices = {"Z": lambda: self.model(data.inner).predict(data.X)}
        if "probability" in self.config and self.config["probability"]:
            matrices["P"] = lambda: self.model(data.inner).predict_proba(data.X)
        return data.update(self, **matrices)

    # @globalcache
    def model(self, data):
        """Predictor model induced on the training set.

        This cached method is needed because the so called "model" is called more than once inside process()."""
        model = self.algorithm
        model.fit(*data.Xy)
        return model

    @property
    def algorithm(self):
        return self._algorithm_func()()

    @abstractmethod
    def _algorithm_func(self):
        pass

    # x = 0.00001
    # l = []
    # for i in range(128):
    #     x = x * 1.1
    #     l.append(x)
    # print(l)

    """
default = SVM(tr).process(ts)
default = SVM(tr).process([tr, ts])
default = SVM(tr).process([ts1, ts2, ts3])
simples = SVM(tr, ...).process(d)
workf = File("iris") * Bin * Split(...) * dual(PCA(n=5) * dual(SVM(...))
expr = File("iris") * Split(...) * PCA(tr) * SVM(tr)

                                -> ts{tr}
expr = File("iris") * Split(...) * dual(NR(), Id()) * dual(PCA()) * dual(Id(), SVM())
Split(...) * PCA() * SVM()
= Chain(Split(...), dual(PCA())) * SVM()
= Chain(Split(...), dual(PCA()), dual(SVM()))

expr.process(ts)
expr.sample(ts).process(ts)
    
SVM(tr).process(ts)       ->  default
SVM(tr, ...).process(ts)  ->  configured

SVM(tr).sample()            ->  random
SVM(tr, ...).sample()       ->  partially configured/random
  
SVM()(tr).process(ts)     ->  default
SVM().sample()              ->  SVM(...)
SVM().sample()(tr)          ->  random
SVM(...)                    ->  lambda  
SVM(...)(tr).process(tr)  ->  configured
SVM(...)(tr).sample(ts)     ->  partially configured/random

Todo step transforma o data passado (externo).
Alguns dependem do data interno (trdata) como dado de entrada.
Para alterar dado interno, há dois modificadores: Inner e Both
Inner(NR()) -> aplica no trdata [mas transforma ambos! histórico: InnerNR muda o de fora e NR o de dentro]
Both(PCA()) -> aplica em ambos, mas treina sempre no interno [histórico: BothPCA muda externo e PCA muda interno] 
    """
