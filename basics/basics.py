from functools import reduce
from abc import ABC,abstractmethod

# Function : posi & keyword arg
def sub(a,b):
    return a-b

# Function : *args & **kwargs
def add(*args,**kwargs):
    return f"*args as tuple : {args}\n**kwargs as dict : {kwargs}"

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

    print("Main Block\n----------------------")
# creating Emp class obj
    print("Creating Obj var a,b,c of Emp Class\n----------------------")
    a=Emp('surya',1)
    b=Emp('dsp',2)
    c=Emp('krishna',3)

# Class var
    print("Class Var Id\n----------------------")
    print(f"no of obj of Emp : {Emp.id}\n")

# private var
    print("Private var\n----------------------")
    print(f"Emp name of obj a : {a.getName()}\n")

# static method call
    print("Static Method call\n----------------------")
    print(f"static method : {a.lpa(2000)}\n")

# instnace method call
    print("Instance Method call\n----------------------")
    print(f"instance method : {a.getDetails('surya')}\n")

# Class Method -> making class var to 0
    print("Class Method call\n----------------------")
    print(f"{Emp.zeroId()}\n")
    
# creating Info class obj
    print("Creating Obj var i of Info Class\n----------------------")
    i = Info('bannu',1,'SSE')
    print(f"no of obj of i : {Emp.id}\n")

    print("Abs method impl\n----------------------")
    print(f"{i.getDetails()}\n")
    
# Method over wirtting 
    print("Method Overwritting\n----------------------")
    print(f"{i.name_obj()}\n")

# Dunder Metod
    # __str__
    print("DUNDER FUNC\n----------------------")
    print(f"a : {a}")
    print(f"i : {i}\n")

    # __lt__
    print(f"sal of i is less then a : {i<a}\n")

# Lambda func
    print("Lambda Func\n----------------------")
    print(f"{(lambda x,y : "even" if x%2 ==0 else "odd" )(4,2)}\n" )

# Map()
    print("Map Func\n----------------------")
    print(f"Map func : {list(map(lambda a: f"{a} even" if a%2==0 else f"{a} odd",list([x for x in range(1,11)])))}\n")

# Filter()
    print("Filter Func\n----------------------")
    print(f"Filter func : {list(filter(lambda x: 1 if x%2==0 else 0,list([x for x in range(1,11)]) ))}\n")

# Reduce()
    print("Reduce Func\n----------------------")
    print(f"Reduce func : {reduce(lambda x,y:x+y,list([x for x in range(1,11)]))}\n")

# Decarator func
    print("Decorator\n----------------------")
    base()

# input
    print("Input\n-----------------------------")
    x = int(input("enter value for x"))
    y = int(input("enter value for y"))

# Function
    print(f"\nFunction\n----------------------")
    print(f"positional arg : {sub(x,y)}")
    print(f"keyword arg : {sub(b=y,a=x)}")
    print(add(1,2,3,a=1,b=2))

# execption handling
try:

# prevention of main code to be not used in-directly
    if __name__ == '__main__':
        main()
    else:
        print("calling from non main file")
except ValueError:
    print("please enter int value")
except:
    print("something went wrong")
finally:
    print("------------------------Execution successfull------------------------------------")


