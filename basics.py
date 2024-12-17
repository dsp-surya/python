from functools import reduce
from abc import ABC,abstractmethod
# Abstract class
class Emp(ABC):

# Abstract Method
    @abstractmethod
    def getDetails(self):
        pass

# Class var
    id = 0

# Constructor
    def __init__(self,name,sal):

# private var
        self.__name = name
        self.sal = sal
        Emp.id+=1
    
# Instance Method
    def getName(self):
        return self.__name
    def getDetails(self,name):
        return f'abstract implemented in {name} and sal is {Emp.lpa(2000)}'

    def name_obj(self):
        return f"name of obj is {self.__name}"
    
# Static Method
    @staticmethod
    def lpa(sal):
        return sal*12
    
# Class method
    @classmethod
    def zeroId(cls):
        cls.id = 0
        return "Class var Id is modified to 0"
# Dunder func
    def __str__(self):
        return f"the Emp name is {self.__name}"
    
    def __lt__(self,other):
        return self.sal < other.sal

# Inheritance
class Info(Emp):
    def __init__(self, name, sal,role):

# Super func
        super().__init__(name,sal)
        self.role = role

# Abstract method mandatorilly to be implemented
    def getDetails(self):
        return f"abstract implemented"

# Method overwritting
    def name_obj(self):
        return f"Method overwritting obj name is {self.getName()}"

# Decorator

def Deco(base):
    def wrap():
        print("decoratoring the base func")
        base()
    return wrap
    
@Deco
def base():
    print("this is the base func")

# ---------------------Main Func-----------------------------------
def main():

    print("--------------------Main Block-------------------------\n")
# creating Emp class obj
    print("-------------------Creating Obj var a,b,c of Emp Class-----------------------\n")
    a=Emp('surya',1)
    b=Emp('dsp',2)
    c=Emp('krishna',3)

# Class var
    print("-------------------Class Var Id----------------------\n")
    print(f"no of obj of Emp : {Emp.id}")

# private var
    print("------------------------Private var----------------------\n")
    print(f"Emp name of obj a : {a.getName()}")

# static method call
    print("---------------------------Static Method call---------------------\n")
    print(f"static method : {a.lpa(2000)}")

# instnace method call
    print("--------------------------------Instance Method call-------------------------------\n")
    print(f"instance method : {a.getDetails('surya')}")

# Class Method -> making class var to 0
    print("------------------------------Class Method call-------------------------------------\n")
    print(Emp.zeroId())
    
# creating Info class obj
    print("-----------------------Creating Obj var i of Info Class--------------------------------\n")
    i = Info('bannu',1,'SSE')
    print(f"no of obj of i : {Emp.id}")

    print("-------------------------Abs method impl----------------------\n")
    print(f"{i.getDetails()}")
    
# Method over wirtting 
    print("---------------------Method Overwritting-------------------------------\n")
    print(f"{i.name_obj()}")

# Dunder Metod
    # __str__
    print("-------------------------DUNDER FUNC-------------------------------\n")
    print(f"a : {a}")
    print(f"i : {i}")

    # __lt__
    print(f"sal of i is less then a : {i<a}")

# Lambda func
    print("----------------------------Lambda Func-------------------\n")
    print(f"{(lambda x,y : "even" if x%2 ==0 else "odd" )(4,2)}" )

# Map()
    print("----------------------------Map Func-------------------\n")
    print(f"Map func : {list(map(lambda a: f"{a} even" if a%2==0 else f"{a} odd",list([x for x in range(1,11)])))}")

# Filter()
    print("----------------------------Filter Func-------------------\n")
    print(f"Filter func : {list(filter(lambda x: 1 if x%2==0 else 0,list([x for x in range(1,11)]) ))}")

# Reduce()
    print("----------------------------Reduce Func-------------------\n")
    print(f"Reduce func : {reduce(lambda x,y:x+y,list([x for x in range(1,11)]))}")

# Decarator func
    print("-------------------------Decorator--------------------------------\n")
    base()

# prevention of main code to be not used in-directly
if __name__ == '__main__':
    main()
else:
    print("calling from non main file")

