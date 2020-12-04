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

from dataclasses import dataclass
from typing import Iterator

from akangatu.linalghelper import islazy


@dataclass
class Result:
    value: float


class InterruptedStreamException(Exception):
    pass


class Accumulator(Iterator):
    """Cumulative iterator that returns a final/result value.

    The enclosed iterator should be finite."""

    def __init__(self, iterator, start, step_func, end_func, stream_exception=False):
        self.iterator = iterator
        self.start = start
        self.step_func = step_func
        self.end_func = end_func
        self.stream_exception = stream_exception

    def __next__(self):
        raise NotImplemented

    @property
    def result(self):
        if self.stream_exception:
            raise InterruptedStreamException
        try:
            return self._result
        except AttributeError as e:
            print("Stream not consumed!\nHINT: The result of summarizers are only accessible after Reduce.")
            exit()
            # raise e from None

    def __iter__(self):
        acc = self.start.copy()
        self.iterator = self.iterator() if islazy(self.iterator) else self.iterator
        try:
            for data in self.iterator:
                dic={"data":data}
                if not self.stream_exception:
                    dic = self.step_func(data, acc)
                    # if step is XXXXX:
                    #     self.stream_exception = True
                    # else:
                    if "inc" in dic:
                        # REMINDER: doesn't need to be thread-safe, since processing of iterator is always sequential
                        acc.append(dic["inc"])
                yield dic["data"]
        finally:
            if not self.stream_exception:
                self._result = self.end_func(acc)
