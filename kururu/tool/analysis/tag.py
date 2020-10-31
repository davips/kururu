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

# import threading
#
# from akangatu.abs.container import Container1
# # from transf.mixin.noop import asNoOp
#
#
# class Tag(asNoOp, Container1):
#     """alias=None -> this is the default tag and can be accessed through the 'tag' property of an expression."""
#     threadLock = threading.Lock()
#     number = -1
#
#     def __new__(cls, *args, **kwargs):
#     instance = super(Tag, cls).__new__(cls)
#     # REMINDER: All Tags are ordered, the first ones have higher priority.
#     # Also, 'number' identifies them uniquely and "marks" them as result of an unsafe (i.e. mutable) method.
#     with cls.threadLock:
#         cls.number += 1
#     instance.number = cls.number
#     return instance
#
#     def __init__(self, step, alias=None):
#     super().__init__(step, {"alias": alias})
#     self.alias = alias
#     self.used = False
#
#     def _process_(self, data):
#     if self.used:
#         print("Cannot reuse a Tag step! Used with:", self.input.id, self.output.id)
#         exit()
#     with Tag.threadLock:
#         self.used = True
#         self.input = data
#     output = self.step.process(data)
#     with Tag.threadLock:
#         self.output = output
#     return output
#
#     @property
#     def model(self):
#     if not self.used:
#         print("Unused Tag step!")
#         exit()
#     return self.step.model(self.input)
#
#     def __getitem__(self, item):
#     if not self.used:
#         print("Unused Tag step!")
#         exit()
#     if "tags" not in dir(self.step):
#         print("Cannot get tag from a contained step without tags:", self.step.longname)
#         exit()
#     tags = self.step.tags
#     if item not in tags:
#         print(f"Missing tag {item}!")
#         exit()
#     return tags[item]   #(self.input)
