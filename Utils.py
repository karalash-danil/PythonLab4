import csv
import json
import os
import pickle


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

class Transport:
    def __init__(self, m: str="", b: str="", s: float=0.0, y: int=2000, mo: str="", c: str="", p: float=0, se: int=1) -> None:
        self.id = -1

        self.name = "Транспорт"

        self.model = m
        self.brand = b
        self.speed = s
        self.seats = se

        self.year = y
        self.month = mo

        self.color = c

        self.price = p

        self.imageId = 0
        self.image = None

class Car(Transport):
    def __init__(self,*args,f:str="",**kwargs):
        super().__init__(*args,**kwargs)
        self.name = "Автомобіль"

        self.fuelType = f

class ListData:
    def __init__(self, id: str, name="", values=None, max=100):
        if values is None:
            values = []
        self.id = id
        self.name = name
        self.values = values
        self.max = max

        self._Changed = Event()

        self._FullChanged = Event()

        self._AddedValue = Event()
        self._ChangedValue = Event()
        self._RemovedValue = Event()

        self._Changed.add(ListsDataBase()._Changed.fire)

    def pack_data(self):
        return {"name": self.name, "values": self.values, "max": self.max}

    def append(self, value):
        self.values.append(value)
        self._AddedValue.fire(len(self.values)-1, value)
        self._Changed.fire()

    def insert(self, index, value):
        self.values.insert(index, value)
        self._AddedValue.fire(index, value)
        self._Changed.fire()

    def pop(self, index: int):
        v = self.values[index]
        self.values.pop(index)
        self._RemovedValue.fire(index, v)
        self._Changed.fire()

    def remove(self, value):
        i = self.values.index(value)
        self.values.remove(value)
        self._RemovedValue.fire(i, value)
        self._Changed.fire()

    def index(self, value) -> int:
        return self.values.index(value)

    def has(self, value) -> bool:
        return value in self.values

    def size(self) -> int:
        return len(self.values)

    def change(self, index: int, value):
        self.values[index] = value
        self._ChangedValue.fire(index, value)
        self._Changed.fire()

    def sort(self):
        self.values.sort()
        self._FullChanged.fire()
        self._Changed.fire()

    def reverse(self):
        self.values.reverse()
        self._FullChanged.fire()
        self._Changed.fire()

@singleton
class ListsDataBase:
    def __init__(self):
        self.data = {}

        self._Changed = Event()

        self._AddedListData = Event()
        self._ChangedListData = Event()
        self._RemovedListData = Event()

        self._Changed.add(self.save)

    def save(self):
        data = {"data": {}}

        for i in self.data.keys():
            data["data"].update({i:self.data[i].pack_data()})

        print(data)

        with open('lists.json', 'w', encoding="UTF-8") as file:
            json.dump(data, file, ensure_ascii=False)

    def load(self):
        with open('lists.json', 'r', encoding="UTF-8") as file:
            try:
                data = json.load(file)

                if "data" in data and type(data["data"]) is dict:
                    for i in data["data"].keys():
                        self.create(i, data["data"][i]["name"], data["data"][i]["values"])

                print(self.data)
            except Exception as e:
                print(e)

    def create(self, id:str, name="", values=None, max=100):
        if not(type(id) is str): return None
        if id in self.data: return self.data[id]
        if values is None: values = []

        obj = ListData(id,name,values,max)
        self.data.update({id:obj})
        self._AddedListData.fire(len(self.data)-1, obj)
        self._Changed.fire()
        return obj

    def get(self, id:str):
        if id not in self.data:
            return None
        return self.data[id]

    def getNames(self):
        result = []
        for i in self.data.keys():
            result.append(self.data[i].name)
        return result

@singleton
class ObjectsDataBase:
    def __init__(self):
        self.data = []

    def loadAll(self):
        try:
            with open(f'objects.bin', 'rb') as file:
                _data = pickle.load(file)

                for data in _data:
                    obj = self.create()
                    obj.model = data["m"]
                    obj.brand = data["b"]
                    obj.speed = float(data["s"])
                    obj.seats = int(data["se"])
                    obj.year = int(data["y"])
                    obj.month = data["mo"]
                    obj.color = data["c"]
                    obj.imageId = int(data["i"])
                    obj.price = float(data["p"])
                    obj.fuelType = data["ft"]
        except Exception as e:
            pass

    def loadFromFolder(self):
        for i in os.listdir("objects"):
            with open(f'objects/{i}', 'r', encoding="UTF-8") as file:
                try:
                    data = {}

                    for line in csv.reader(file):
                        if len(line) > 1:
                            data[line[0]] = line[1]

                    obj = self.create()
                    obj.model = data["m"]
                    obj.brand = data["b"]
                    obj.speed = float(data["s"])
                    obj.seats = int(data["se"])
                    obj.year = float(data["y"])
                    obj.month = data["mo"]
                    obj.color = data["c"]
                    obj.imageId = int(data["i"])
                    obj.price = float(data["p"])
                    obj.fuelType = data["ft"]
                except Exception as e:
                    pass

    def create(self):
        obj = Car()
        self.data.append(obj)
        obj.id = len(self.data)-1
        return obj

    def saveAll(self):
        with open(f'objects.bin', 'wb') as file:
            data = []

            for obj in self.data:
                data.append({
                    "m": obj.model,
                    "b": obj.brand,
                    "s": obj.speed,
                    "se": obj.seats,
                    "y": obj.year,
                    "mo": obj.month,
                    "c": obj.color,
                    "p": obj.price,
                    "i": obj.imageId,
                    "ft": obj.imageId
                })

            pickle.dump(data, file)

    def importObject(self, path):
        with open(path, 'r', encoding="UTF-8") as file:
            try:
                data = {}

                for line in csv.reader(file):
                    if len(line) > 1:
                        data[line[0]] = line[1]

                obj = self.create()
                obj.model = data["m"]
                obj.brand = data["b"]
                obj.speed = float(data["s"])
                obj.seats = int(data["se"])
                obj.year = int(data["y"])
                obj.month = data["mo"]
                obj.color = data["c"]
                obj.imageId = int(data["i"])
                obj.price = float(data["p"])
                obj.fuelType = data["ft"]

                return obj
            except Exception as e:
                pass

    def exportObject(self, obj, path=None):
        _path = path if path else f'export/{obj.id}.csv'

        with open(_path, 'w', encoding="UTF-8") as file:
            data = {
                "m": obj.model,
                "b": obj.brand,
                "s": obj.speed,
                "se": obj.seats,
                "y": obj.year,
                "mo": obj.month,
                "c": obj.color,
                "p": obj.price,
                "i": obj.imageId,
                "ft": obj.imageId
            }
            writer = csv.writer(file)
            # Write data
            for key, value in data.items():
                writer.writerow([key, value])

    def save(self, obj):
        self.saveAll()

    def get(self, id):
        return self.data[id]

    def delete(self, id):
        del self.data[id]
        for i in range(id,len(self.data)):
            self.data[i].id -= 1

        if os.path.exists(f'objects/{id}.csv'):
            os.remove(f"objects/{id}.csv")

class Event:
    def __init__(self):
        self.funcs = []

    def add(self, func):
        self.funcs.append(func)

    def remove(self, func):
        self.funcs.remove(func)

    def has(self, func):
        return func in self.funcs

    def fire(self, *args):
        for func in self.funcs:
            func(*args)

# - Initing DataBases -----------------

ObjectsDataBase().loadAll()
ListsDataBase().load()