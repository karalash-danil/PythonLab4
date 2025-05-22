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
    def __init__(self, name="", values=None, max=100):
        if values is None:
            values = []
        self.name = name
        self.values = values
        self.max = max

@singleton
class ListsDataBase:
    def __init__(self):
        self.data = {}

    def create(self, id:str, name="", values=None, max=100):
        if not(type(id) is str): return None
        if id in self.data: return self.data[id]
        if values is None: values = []

        obj = ListData(name,values,max)
        self.data.update({id:obj})
        self._AddedListData.fire(len(self.data)-1, obj)
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

    def create(self):
        obj = Car()
        self.data.append(obj)
        obj.id = len(self.data)-1
        return obj

    def save(self, id, obj):
        self.data[id] = obj

    def get(self, id):
        return self.data[id]

    def delete(self, id):
        del self.data[id]
        for i in range(id,len(self.data)):
            self.data[i].id -= 1

# - Initing DataBases -----------------

car1 = ObjectsDataBase().create()
car1.model = "LX 12"
car1.brand = "Lexus"
car1.imageId = 0
car1.color = "Блакитний"
car1.price = 24500
car1.seats = 4
car1.year = 2007
car1.month = "Травень"
car1.speed = 240
car1.fuelType = "Газ / Бензин"

car2 = ObjectsDataBase().create()
car2.model = "FE"
car2.brand = "Hyundai"
car2.imageId = 1
car2.color = "Жовтий"
car2.price = 20500
car2.seats = 3
car2.year = 2012
car2.month = "Березень"
car2.speed = 120
car2.fuelType = "Газ"


ListsDataBase().create("brand","Бренд",["BMW", "Ford", "Audi", "Mazda", "Hyundai", "Toyota", "Honda", "Lexus"])
ListsDataBase().create("color","Колір",["Білий", "Сірий", "Чорний", "Червоний", "Блакитний", "Жовтий", "Зелений"])
ListsDataBase().create("month","Місяць",["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень", "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"], 12)
ListsDataBase().create("fuelType","Тип палива",["Бензин", "Дизель", "Газ", "Газ / Бензин", "Електро", "Гібрид"])