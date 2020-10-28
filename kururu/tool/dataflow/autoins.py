from akangatu.distep import DIStep
from transf.mixin.config import asConfigLess


class AutoIns(asConfigLess, DIStep):
    def _process_(self, data):
        # Forbid("inner").process(data)
        # # inner = lambda: Del("stream").process(data)  # blank stream to avoid confusion with two pointers to the same iterator
        if "stream" in data:
            print("W: field \"stream\" in data while auto inserting")
            print("HINT: you may want to blank the stream field to avoid confusion with two pointers to the same iterator.")
        return data.update(self, inner=lambda: data)
