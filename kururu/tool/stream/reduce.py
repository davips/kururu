from akangatu.distep import DIStep
from transf.mixin.config import asConfigLess


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
#         return Reduce * In(Reduce)  # REMINDER: talvez um dia faça sentido
