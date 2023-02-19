# coding: utf-8

def runtime_import(modulename, name):
    """ Import a named object from a module in the context of this function.
    """
    try:
        module = __import__(modulename, globals(), locals(  ), [name])
    except ImportError:
        return None
    return vars(module)[name]

# * ... lol: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch15s04.html
