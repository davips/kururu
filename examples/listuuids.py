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
    # if not data.hasinner or not callable(step):
    print("data.inner", data.uuid * step.uuid, res.uuid, data.uuid * step.uuid == res.uuid, end="  ")
    print(res.field_funcs_m, end="  ")
    print(res.hasinner and res.inner.field_funcs_m)
    # else:
    #     print("   (data)", Ins(data).process(data).uuid * step.uuid, res.uuid, Ins(data).process(data).uuid * step.uuid == res.uuid)
    #     print(" esperado ", Ins(data).process(data).uuid, "*", step.uuid, "=", Ins(data).process(data).uuid * step.uuid)
    #     print(" ocorrido ", data.uuid, "*", step.uuid, "=", res.uuid)
