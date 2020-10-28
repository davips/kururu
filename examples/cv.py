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
from kururu.tool.communication.lazycache import LCache
from kururu.tool.communication.report import Report
from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.enhancement.binarize import Binarize
from kururu.tool.enhancement.pca import PCA
from kururu.tool.evaluation.metric import Metric2
from kururu.tool.evaluation.partition import Partition
from kururu.tool.evaluation.summ import Summ2, Summ
from kururu.tool.learning.supervised.classification.svm import SVM2
from kururu.tool.stream.map import Map
from kururu.tool.stream.reduce import Reduce
from tatu.sql.mysql import MySQL
from tatu.sql.sqlite import SQLite

f = File("iris.arff")

# SQLite().delete_data(f.data, check_existence=False)
my = MySQL(db="tatu:kururu@localhost/tatu",threaded=False)
my.open()
my.store(f.data >> AutoIns * PCA)
print((f.data >> AutoIns * PCA).id)
print(my.fetch((f.data >> AutoIns * PCA).id, lazy=False).history^"name", (f.data >> AutoIns * PCA).id)
exit()
#






#
# sq = SQLite()
#
# print(f.data.Xd)
# # my.store(f.data)
#
#
#
d = f.data
# print("antes:\n", list(d.history ^ "id"), d.id)
# print(d.Y[:2])

print('---------------')
d = d >> LCache(my)
d.Y
print("depois:\n", list(d.history ^ "name"))

# print(d)
print(d.Y[:2])

d = my.fetch("3l9bSwFwL0TsSztkDb0iuVQ", lazy=False)
print(d.history^"name", d.Y)
# print(d.arff("nome", "desc"))
exit()

print("---------------- ========================= +++++++++++++++++++++++++++++")
pipe = PCA(n=3) * SVM2(C=1) * Metric2(["accuracy", "history"])
wk = File("abalone3.arff") * Binarize * Partition(splits=3) * Map(pipe * Report("$r {inner.r}")) * Summ2 * Reduce
data = wk.data
# data = wk.sample().data
print("train:\n", data.Si)
print("test:\n", data.S, list(data.history ^ "name"))

# cache e streamcache?   cache seria como summ, que finaliza usando Accumulator
