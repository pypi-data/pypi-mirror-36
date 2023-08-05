from collections.abc import MutableMapping

class Vertex(MutableMapping):
    instances = []

    def __init__(self, x=None, y=None, z=None, *args, **kw):
        if x is None or y is None or z is None:
            raise ValueError("(x,y,z) cannot contain null values")
        self._storage = dict(x=x,y=y,z=z,name=None,*args, **kw)
        Vertex.instances.append(self)

    def __getitem__(self, key):
        return self._storage[key]
    def __setitem__(self, key, value):
        self._storage[key] = value
    def __delitem__(self, key):
        del self._storage[key]
    def __len__(self):
        return len(self._storage)
    def __iter__(self):
        return iter(self._storage)
    def __len__(self):
        return len(self._storage)
    def __repr__(self):
        string = "("+str(self["x"])+" "+str(self["y"])+" "+str(self["z"])+")"
        return string
    def __eq__(self, other):
        if type(other) is type(self):
            if self["x"] is other["x"] and self["y"] is other["y"] and self["z"] is other["z"]:
               return True
        else:
            return False
    def __add__(self, other):
        return Vertex(self["x"] + other["x"],
                      self["y"] + other["y"],
                      self["z"] + other["z"])

    def __sub__(self, other):
        return Vertex(self["x"] - other["x"],
                      self["y"] - other["y"],
                      self["z"] - other["z"])
    def __lt__(self,other):
        x = self["x"] < other["x"]
        y = self["y"] < other["y"]
        z = self["z"] < other["z"]

        x1 = self["x"] == other["x"]
        y1 = self["y"] == other["y"]
        z1 = self["z"] == other["z"]

        if x and not x1:
            return True
        elif x1:
            if y and not y1:
                return True
            elif y1:
                if z and not z1:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False



    @classmethod
    def list_all(cls):
        string = "\nvertices\n(" + "\n    " + "\n    ".join([str(vertex) for vertex in cls.instances]) + "\n)"
        return string

    @classmethod
    def assign_names(cls):
        for i,vertex in enumerate(cls.instances):
            vertex["name"] = str(i)
