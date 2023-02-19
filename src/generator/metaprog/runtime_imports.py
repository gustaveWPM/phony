# coding: utf-8

def runtime_import(modulename: str, obj: any):
    try:
        module = __import__(modulename, globals(), locals(  ), [obj])
    except ImportError:
        return None
    return vars(module)[obj]

# * ... lol: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch15s04.html
