# Interface Segregation Principle
# We should not stick too many methods/attributes to an interface

class Machine:
    def print(self, document):
        raise NotImplementedError
    def fax(self, document):
        raise NotImplementedError
    def scan(self, document):
        raise NotImplementedError


class MultiFunctionPrinter(Machine):
    def print(self, document):
        pass
    def fax(self, document):
        pass
    def scan(self, document):
        pass

class OldFashionedPrinter(Machine):
    def print(self, document):
        # Ok
        pass

    def fax(self, document):
        pass # noop

    def scan(self, document):
        raise NotImplementedError('Printer cannot scan!')


## Have different interfaces

class Printer:
    @abstractmethod
    def print(self, document):
        pass

class Scanner:
    @abstractmethod
    def scan(self, document):
        pass

class MyPrinter(Printer):
    def print(self, document):
        print(document)

class Photocopier(Printer, Scanner):
    def print(self, document):
        pass

    def scan(self, document):
        pass
