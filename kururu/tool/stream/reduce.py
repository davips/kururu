from akangatu.distep import DIStep
from transf.absdata import AbsData
from transf.mixin.paramless import asParamLess


class Reduce(asParamLess, DIStep):
    def _process_(self, data: AbsData):
        # TODO: centralizar logs usando essas tecnologias :

        if data.stream is None:
            def debug_print(*arg):
                from inspect import currentframe
                frameinfo = currentframe()
                print(frameinfo.f_back.f_code.co_filename, " Line:", frameinfo.f_back.f_lineno)
                print(*arg)

            debug_print("\nHistory: " + str(data.history) + f"\n{self.name} needs a Data object containing a stream.")
            print("Missing stream inside", data.id)
            exit()

        failures = []  # TODO:checar se falhados estão sendo tratados/interrompidos no Step (caso geral)
        for d in data.stream:
            # print("consome", d.id)
            if d.failure:
                failures.append(d.failure)
        if failures:
            data = data.failed([], "; ".join(failures))
        return data.replace(self, stream=None)


# class Reduce2(asMacro, Reduce):
#     def _step_(self):
#         return Reduce * In(Reduce)  # REMINDER: talvez um dia faça sentido
