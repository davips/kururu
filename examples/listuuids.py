from aiuna.step.file import File
from kururu.tool.enhancement.attribute.pca import PCA
from kururu.tool.evaluation.metric import Metric2
from kururu.tool.evaluation.partition import Partition
from kururu.tool.evaluation.split import Split, Split1
from kururu.tool.learning.supervised.classification.svm import SVM2
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
    # if not data.hasinner or not callable(step):
    print("data.inner", data.uuid * step.uuid, res.uuid, data.uuid * step.uuid == res.uuid, end="  ")
    print(res.field_funcs_m, end="  ")
    print(res.hasinner and res.inner.field_funcs_m)
    # else:
    #     print("   (data)", Ins(data).process(data).uuid * step.uuid, res.uuid, Ins(data).process(data).uuid * step.uuid == res.uuid)
    #     print(" esperado ", Ins(data).process(data).uuid, "*", step.uuid, "=", Ins(data).process(data).uuid * step.uuid)
    #     print(" ocorrido ", data.uuid, "*", step.uuid, "=", res.uuid)
