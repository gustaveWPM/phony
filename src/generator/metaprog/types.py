# coding: utf-8


Void = None


class Schema(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    def __setattr__(self, key, value):
        if key not in [*self.keys(), '__dict__']:
            raise KeyError(f"Unknown key: {key}")
        else:
            super().__setattr__(key, value)

    def __setitem__(self, key, value):
        if key not in self:
            raise KeyError(f"Unknown key: {key}")
        else:
            super().__setitem__(key, value)

    # * ... see: https://stackoverflow.com/questions/58009864/python-how-to-disable-creation-of-new-keys-in-attribute-dict
