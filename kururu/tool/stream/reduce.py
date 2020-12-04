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

from akangatu.distep import DIStep
from akangatu.transf.mixin.config import asConfigLess


class FailureAtStream(Exception):
    """At least one of the streamed Data objects failed during build."""


class Reduce(asConfigLess, DIStep):
    def _process_(self, data):
        # TODO: centralizar logs usando essas tecnologias :
        def consume():
            if data.stream is None:
                def debug_print(*arg):
                    from inspect import currentframe
                    frameinfo = currentframe()
                    print(frameinfo.f_back.f_code.co_filename, " Line:", frameinfo.f_back.f_lineno)
                    print(*arg)

                debug_print("\nHistory: " + str(data.history) + f"\n{self.name} needs a Data object containing a stream.")
                print("Missing stream inside", data.id)
                exit()

            # print("começa redu")
            failures = []  # TODO:checar se falhados estão sendo tratados/interrompidos no Step (caso geral)
            for d in data.stream:
                # print("consome", d.id)
                if d.failure:
                    print("falhou", d.failure)
                    failures.append(d.failure)
            print("terminou")
            if failures:
                raise FailureAtStream(data.failed([], "; ".join(failures)))
            return

        return data.update(self, stream=consume)

    def translate(self, exception, data):
        if isinstance(exception, FailureAtStream):
            return f"{data.id} stream failures: {str(exception)}"

# class Reduce2(asMacro, Reduce):
#     def _step_(self):
#     return Reduce * In(Reduce)  # REMINDER: talvez um dia faça sentido
