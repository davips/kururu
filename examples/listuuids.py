from aiuna.file import File
from kururu.tool.enhancement.pca import PCA1, PCA
from kururu.tool.evaluation.metric import Metric, Metric2
from kururu.tool.evaluation.partition import Partition
from kururu.tool.evaluation.split import Split, Split1
from kururu.tool.learning.supervised.classification.svm import SVM, SVM2
from kururu.tool.manipulation.slice import Slice
from transf._ins import Ins

data = File("iris.arff").data
# print("------------------")
# data = (File("iris.arff") * Split).data
# steps = [SVM(), SVM2()] #, Metric2(), Metric(), PCA(), PCA1(), Split(), Split1(), Partition(), Slice(), Ins(data)]
steps = [SVM(data), SVM2(data)] #, Metric2(), Metric(), PCA(), PCA1(), Split(), Split1(), Partition(), Slice(), Ins(data)]

for step in steps:
    print(step.name.rjust(25, " "), end="   ")
    print(step.id, end="   ")

    res = step.process(data)
    print(data.uuid * step.uuid, res.uuid)
