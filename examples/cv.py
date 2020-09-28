from aiuna.file import File
from akangatu.operator.unary.inop import In
from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.enhancement.binarize import Binarize
from kururu.tool.enhancement.pca import PCA
from kururu.tool.evaluation.metric import Metric2
from kururu.tool.evaluation.partition import Partition
from kururu.tool.evaluation.split import Split
from kururu.tool.evaluation.summ import Summ2, Summ
from kururu.tool.learning.supervised.classification.svm import SVM2
from kururu.tool.stream.map import Map
from kururu.tool.stream.reduce import Reduce, Reduce2

pipe = PCA(n=3) * SVM2 * Metric2(["accuracy", "history"])
wk = File("abalone3.arff") * Binarize * Partition(splits=3) * Map(pipe) * Summ2 * Reduce2
data = wk.data
print("inner S:", data.inner and data.inner.S)
print("S:", data.S)
# print("train:\n", data.inner.r, list(data.inner.history.clean))
# print("test:\n", data.r, list(data.history.clean))

# Repeat, Partition
# Map
# Summ
# Reduce