from dataclasses import dataclass
from typing import Iterator

from linalghelper import islazy


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
