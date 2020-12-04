from aiuna.step.file import File
from akangatu.abs.delimiter import Begin, End
from akangatu.rev import Rev
from cruipto.uuid import UUID
from kururu.tool.enhancement.attribute.pca import PCA1, PCA
from kururu.tool.evaluation.metric import Metric, Metric2
from kururu.tool.evaluation.partition import Partition
from kururu.tool.evaluation.split import Split, Split1
from kururu.tool.learning.supervised.classification.svm import SVM, SVM2
from kururu.tool.manipulation.slice import Slice
from akangatu.transf._ins import Ins

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
    # t = akangatu.transf(data) if callable(akangatu.transf) else akangatu.transf
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
