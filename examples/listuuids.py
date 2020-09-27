from aiuna.file import File
from cruipto.uuid import UUID
from kururu.tool.enhancement.pca import PCA1, PCA
from kururu.tool.evaluation.metric import Metric, Metric2
from kururu.tool.evaluation.partition import Partition
from kururu.tool.evaluation.split import Split, Split1
from kururu.tool.learning.supervised.classification.svm import SVM, SVM2
from kururu.tool.manipulation.slice import Slice
from transf._ins import Ins

data = File("iris.arff").data
print("iris", data.id)
print("iden", UUID.identity)
for transf in [SVM(), SVM2(), File("iris.arff"), Metric2(), Metric(), PCA(), PCA1(), Split(), Split1(), Partition(), Slice(), Ins(data)]:
    print("name:", transf.name)
    print(transf.id, "\n")
