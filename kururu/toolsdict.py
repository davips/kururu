from pprint import pprint

from akangatu.container import Container1, ContainerN


def set_leaf(tree, branches, leaf):
    """ Set a terminal element to *leaf* within nested dictionaries.
    *branches* defines the path through dictionnaries.

    Example:
    >>> t = {}
    >>> set_leaf(t, ['b1','b2','b3'], 'new_leaf')
    >>> print t
    {'b1': {'b2': {'b3': 'new_leaf'}}}

    https://stackoverflow.com/a/12389499/9681577
    """
    if len(branches) == 1:
        tree[branches[0]] = leaf
        return
    if branches[0] not in tree:
        tree[branches[0]] = {}
    set_leaf(tree[branches[0]], branches[1:], leaf)


def tools_asdict():
    import importlib
    from kururu import tool
    import sys
    import os
    from pathlib import Path
    m = {}
    path = os.path.abspath(tool.__file__)
    startpath = "/".join(path.split("/")[:-1])
    paths = list(Path(startpath).rglob("*.py"))
    for f in paths:
        if not (f.name.startswith("_") or "/stream/" in str(f) or "/abs/" in str(f) or "/mixin/" in str(f)):
            sys.path.append("/".join(str(f).split("/")[:-1]))
            arq = f.name[:-3]
            a = importlib.import_module(arq)
            for k, v in a.__dict__.items():
                if arq == k.lower() and not k.islower():
                    if not issubclass(v, (Container1, ContainerN)):
                        step = v()
                        m[f.name] = {"step": step.desc, "params": step.parameters}

    tree = {}
    for root, dirs, files in os.walk(startpath):
        branches = [startpath]
        if root != startpath:
            relpath = os.path.relpath(root, startpath)
            branches.extend(relpath.split('/'))

        set_leaf(tree, branches, dict([(d, {}) for d in dirs] + [(f, None) for f in files]))

    def clean(tr):
        dic = {}
        if isinstance(tr, dict):
            dic = {}
            for k, v in tr.items():
                if not (k.startswith("_") and k not in ["stream", "abs", "mixin"]):
                    dic[k] = m[k] if k in m else clean(v)
        return dic

    return clean(list(tree.values())[0])


pprint(tools_asdict(), depth=5)
