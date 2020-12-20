#  Copyright (c) 2020. Davi Pereira dos Santos
#  This file is part of the kururu project.
#  Please respect the license - more about this in the section (*) below.
#
#  kururu is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  kururu is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with kururu.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is a crime and is unethical regarding the effort and
#  time spent here.
#  Relevant employers or funding agencies will be notified accordingly.

from .tool.communication.lazycache import Cache
from .tool.communication.report import Report
from .tool.dataflow.autoins import AutoIns
from .tool.enhancement.attribute.binarize import Binarize
from .tool.enhancement.attribute.pca import pca
from .tool.evaluation.partition import Partition
from .tool.evaluation.split import split
from .tool.evaluation.summ import Summ2
from .tool.learning.supervised.classification.svm import svm
from .tool.stream.map import Map
from .tool.stream.reduce import Reduce

from .tool.evaluation.metric import metric
from .tool.enhancement.attribute.binarize import binarize
