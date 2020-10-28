#  Copyright (c) 2020. Davi Pereira dos Santos
#      This file is part of the kururu project.
#      Please respect the license. Removing authorship by any means
#      (by code make up or closing the sources) or ignoring property rights
#      is a crime and is unethical regarding the effort and time spent here.
#      Relevant employers or funding agencies will be notified accordingly.
#
#      kururu is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      kururu is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with kururu.  If not, see <http://www.gnu.org/licenses/>.
#

from aiuna.file import File
from kururu.tool.communication.report import Report
from kururu.tool.dataflow.rank import Rank
from kururu.tool.dataflow.sort import Sort, Sortr
from kururu.tool.evaluation.split import Split
from kururu.tool.evaluation.uncertainty import Margin
from kururu.tool.learning.supervised.classification.svm import SVM
from kururu.tool.manipulation.copy import Copy
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
