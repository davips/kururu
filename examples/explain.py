from aiuna.step.file import File
from kururu.tool.communication.report import Report
from kururu.tool.dataflow.rank import Rank
from kururu.tool.dataflow.sort import Sort, Sortr
from kururu.tool.evaluation.split import Split
from kururu.tool.evaluation.uncertainty import Margin
from kururu.tool.learning.supervised.classification.svm import SVM
from kururu.tool.manipulation.copy_ import Copy
from kururu.tool.manipulation.slice import Slice
from kururu.tool.vizualization.explain import Explain

wk = (File("iris.arff")
      * Split
      * Explain(
            SVM(C=1, probability=True)
            * Margin
            * Copy("X", "Q")
            * Sortr("U,Q")
            * Report(">> $Q")
            * Slice(0, 1, "Q")
            * Report(">>>> $Q")
        )
      )
data = wk.data
# print("train:\n", data.inner.z)
print("test:\n", data.P.shape, list(data.history.clean))
