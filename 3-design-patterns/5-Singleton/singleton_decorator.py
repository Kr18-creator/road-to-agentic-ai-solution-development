"""
Handling Multiple __init__ call and __new__ method is not a good idea. 
We can use decorator to handle this problem.
"""

def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    
    return get_instance

@singleton
class Database:
    def __init__(self):
        print("Database instance created")

if __name__ == "__main__":
    d1 = Database()
    d2 = Database()
    print(d1 == d2)