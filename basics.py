from functools import reduce
from abc import ABC,abstractmethod
class Emp(ABC):
    @abstractmethod
    def getDetails(self):
        pass
    id = 0
    def __init__(self,name,sal):
        self.__name = name
        self.sal = sal
        Emp.id+=1
    
    def getDetails(self,name):
        return f'abstract implemented in {self.__name}'

    def __str__(self):
        return f"the obj name is {self.__name}"
    
    def __lt__(self,other):
        return self.sal < other.sal

class Info(Emp):
    def __init__(self, name, sal,role):
        super().__init__(name,sal)
        self.role = role

    def getDetails(self):
        return f"abstract implemented"

def main():
    a=Emp('surya',1)
    b=Emp('dsp',2)
    c=Emp('krishna',3)
    print(a.getDetails('dsp'))
    i = Info('surya',1,'SSE')
    print(i.getDetails())
    
    print((lambda x,y : "even" if x%2 ==0 else "odd" )(4,2) )

    print(list(map(lambda a: f"{a} even" if a%2==0 else f"{a} odd",list([x for x in range(1,11)]))))

    print(list(filter(lambda x: 1 if x%2==0 else 0,list([x for x in range(1,11)]) )))

    print(reduce(lambda x,y:x+y,list([x for x in range(1,11)])))

if __name__ == '__main__':
    main()
else:
    print("calling from non main file")

