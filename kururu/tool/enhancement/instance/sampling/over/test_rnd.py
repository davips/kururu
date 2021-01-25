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
#

from unittest import TestCase

from pandas import DataFrame

from aiuna.content.root import Root
from aiuna.step.dataset import Dataset

from kururu.tool.dataflow.autoins import AutoIns
from kururu.tool.enhancement.instance.sampling.over.rnd import ROS_, ROS
from kururu.tool.manipulation.slice import Slice


class Test(TestCase):
    def test__ros_(self):
        iris = Root >> Dataset()
        truncated_iris = iris >> Slice(last=119)
        rebalanced_iris = truncated_iris >> ROS_
        self.assertEqual(50, DataFrame(rebalanced_iris.Y).value_counts()["virginica"][0])
        larger_iris = iris >> ROS_(strategy={"virginica": 100, "versicolor": 50, "setosa": 50})
        self.assertEqual(200, len(larger_iris.X))

    def test__ros(self):
        iris = Root >> (Dataset() * AutoIns)
        truncated_iris = iris >> Slice(last=119)
        rebalanced_iris = truncated_iris >> ROS
        self.assertEqual(50, DataFrame(rebalanced_iris.inner.Y).value_counts()["virginica"][0])
        larger_iris = iris >> ROS(strategy={"virginica": 100, "versicolor": 50, "setosa": 50})
        self.assertEqual(200, len(larger_iris.inner.X))
