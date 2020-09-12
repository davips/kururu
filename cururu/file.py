from transf.transformer import Transformer
import hashlib

class File(Transformer):

    def __init__(self, name, path="./", hash=None):
        try:
            with open(f"{path+name}", "r") as f:
                md5 = hashlib.md5(f).di
        except FileNotFoundError:
            raise Exception(f"Impossible to sample. Missing parameters file: {self.name}.json!")
        self.config = kwargs

    def _transform(self, data):
        pass