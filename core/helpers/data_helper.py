class DataHelper:
    pass


class DotDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

    def _allowDotting(self, state=True):
        if state:
            self.__dict__ = self
        else:
            self.__dict__ = dict()

    def __getattr__(self, item):
        if item not in self.__dict__:
            return None
            # print self.__dict__


