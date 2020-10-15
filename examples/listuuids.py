from aiuna.file import File
from kururu.tool.enhancement.pca import PCA1, PCA
from kururu.tool.evaluation.metric import Metric, Metric2
from kururu.tool.evaluation.partition import Partition
from kururu.tool.evaluation.split import Split, Split1
from kururu.tool.learning.supervised.classification.svm import SVM, SVM2
from kururu.tool.manipulation.slice import Slice
from transf._ins import Ins

data = File("iris.arff").data
# data = Ins(data).process(data)
# print("------------------")
# data = (File("iris.arff") * Split).data
# steps = [SVM(), SVM2()] #, Metric2(), Metric(), PCA(), PCA1(), Split(), Split1(), Partition(), Slice(), Ins(data)]
steps = [PCA(data) * SVM2() * Metric2(), SVM2(data) * Metric2(), Split(), Split1(), Partition(), Slice(), Ins(data)]

for step in steps:
    print(step.longname.rjust(25, " "), end="  ")
    print(step.id, end="  ")

    res = step.process(data)
    # if not data.inner or not callable(step):
    print("data.inner", data.uuid * step.uuid, res.uuid, data.uuid * step.uuid == res.uuid, end="  ")
    print(res.fields, end="  ")
    print(res.inner and res.inner.fields)
    # else:
    #     print("   (data)", Ins(data).process(data).uuid * step.uuid, res.uuid, Ins(data).process(data).uuid * step.uuid == res.uuid)
    #     print(" esperado ", Ins(data).process(data).uuid, "*", step.uuid, "=", Ins(data).process(data).uuid * step.uuid)
    #     print(" ocorrido ", data.uuid, "*", step.uuid, "=", res.uuid)
