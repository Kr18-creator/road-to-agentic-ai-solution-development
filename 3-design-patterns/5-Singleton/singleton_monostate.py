class CEO:
    __shared_state = {
        'name': 'Harry Potter',
        'age': 55
    }

    def __init__(self):
        self.__dict__ = self.__shared_state

    def __str__(self):
        return f'{self.name} is {self.age} years old.'
    
class Monostate:
    _shared_state = {}
    
if __name__ == "__main__":
    ceo1 = CEO()
    print(ceo1)

    ceo2 = CEO()
    ceo2.age = 77
    print(ceo1)
    print(ceo2)