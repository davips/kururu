from aiuna.file import File
from kururu.tool.communication.cache import Cache
from kururu.tool.enhancement.binarize import Binarize
from kururu.tool.enhancement.pca import PCA
from kururu.tool.evaluation.metric import Metric2
from kururu.tool.evaluation.partition import Partition
from kururu.tool.evaluation.summ import Summ2, Summ
from kururu.tool.learning.supervised.classification.svm import SVM2
from kururu.tool.stream.map import Map
from kururu.tool.stream.reduce import Reduce

pipe = PCA(n=3) * SVM2(C=1) * Metric2(["accuracy", "history"])
wk = File("abalone3.arff") * Binarize * Partition(splits=3) * Map(Cache(pipe)) * Summ2 * Reduce
data = wk.data
# data = wk.sample().data
print("train:\n", data.Si)
print("test:\n", data.S, list(data.history.clean))

# cache e streamcache?   cache seria como summ, que finaliza usando Accumulator
