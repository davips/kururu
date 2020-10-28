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
from akangatu.abs.delimiter import Begin, End
from akangatu.rev import Rev
from cruipto.uuid import UUID
from kururu.tool.enhancement.pca import PCA1, PCA
from kururu.tool.evaluation.metric import Metric, Metric2
from kururu.tool.evaluation.partition import Partition
from kururu.tool.evaluation.split import Split, Split1
from kururu.tool.learning.supervised.classification.svm import SVM, SVM2
from kururu.tool.manipulation.slice import Slice
from transf._ins import Ins

l = ['5ȌșNǰǎǦҪɧʌƁΕÖȺ', '0ĬχŌjӓʅřӛȋφȮͶӸ', '2ΑɸȂȈFʘўȚńϝфոŅ', '2ƪȫȮȘʌĘƞղёŷυƼӸ', '3lթŔeǨѳȆźȺλρŝƹ', '0ÓÞŕǢÔơǨǝķϔҢǬŊ', '3ҳāͿΏŦƙUtԚѝȗКӑ', 'äŐȠъīĺǛíǡңipƝչ']
uu = UUID.identity
for u in l:
    uu *= UUID(u)
    print(uu)
print("-------------------")

data = File("iris.arff").tr()
duuid = data.uuid

print(SVM2(data).id)
r = Begin(SVM2(data))
print(r.id)
print(r.uuid.t.id)
print(r.uuid * r.uuid.t)
print((End(SVM2(data)) * Rev(End(SVM2(data)))).id)
# print(UUID('2ΑɸȂȈFʘўȚńϝфոŅ') * UUID('2ƪȫȮȘʌĘƞղёŷυƼӸ'))
print("-------------------")
# exit()

for transf in [SVM(), SVM2(), File("iris.arff"), Metric2(), Metric(), PCA(), PCA1(), Split(), Split1(), Partition(), Slice(), Ins(data)]:
    print(transf.name, end=" ; ")
    # t = transf(data) if callable(transf) else transf
    t=transf
    if callable(transf):
        data.inner=data
    else:
        data.inner=?????????

    dat = None if isinstance(transf, File) else data
    d = t.tr(dat)
    print(duuid, "*", t.id, " -> ", duuid * t.uuid, "  =  ", d.id, " ?")
    if duuid * t.uuid != d.uuid:
        print(d.history)
        print([s.id for s in d.history])
