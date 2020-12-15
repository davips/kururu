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

import re
from abc import ABC

import numpy as np
from aiuna.content.data import Data

from akangatu.distep import DIStep
from garoupa.util import flatten
from akangatu.transf.mixin.noop import asNoOp
from akangatu.transf.mixin.config import asUnitset


class AbsLog(asUnitset, DIStep, ABC):
    """Parent of Log and Report."""

    # TODO: Which matrix are prioritary by default?
    def __init__(self, text="Default log r=$r"):
        super().__init__(text=text)
        self.text = text

    @classmethod
    def _interpolate(cls, text, data):
        # TODO: Check how to set to re-prettify line breaks from numpy arrays.
        def samerow(M):
            return np.array_repr(M).replace("\n      ", "").replace("  ", "")

        def f(obj_match):
            field = obj_match.group(1)
            M = data.field(field, context=cls)
            if isinstance(M, np.float64):
                return str(M)
            try:
                if np.issubdtype(M, np.number):
                    return samerow(np.round(M, decimals=4))
            finally:
                return samerow(M)

        p = re.compile(r"\$([~a-zA-Z]+)")
        return cls._eval(p.sub(f, text), data)

    @classmethod
    def _eval(cls, text, data):
        txt = ""
        run = False
        expanded = [w.split("}") for w in ("_" + text + "_").split("{")]
        for seg in flatten(expanded):
            if run:
                code = "data." + seg
                try:
                    # Convert mapping through ~ operand.
                    if "~" in seg:
                        iterable, accessor = seg.split("~")
                        code = f"[item.{accessor} for item in data.{iterable}]"
                    if "^" in seg:
                        iterable, accessor = seg.split("^")
                        code = f"data.{iterable} ^ '{accessor}'"

                    # Data cannot be changed, so we don't use exec, which would accept dangerous assignments.
                    txt += str(eval(code))
                except Exception as e:
                    print(f"Problems parsing\n  {text}\nwith data\n  {data}\n" f"{data.history}\n!")
                    raise e
            else:
                txt += seg
            run = not run
        return txt[1:][:-1]


class Log(asNoOp, AbsLog):
    """Same as Report, but invisible in History"""

    def _process_(self, data: Data):  # overriding Report, to be invisible
        print(self._interpolate(self.text, data))
        return data
