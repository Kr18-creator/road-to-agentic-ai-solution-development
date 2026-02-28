# Single Responsibility Principle/Separation of Concerns
# A Class should have a primary responsibility and it should not take on other responsibility

class Journal:
    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.count += 1
        self.entries.append(f'{self.count}: {text}')

    def remove_entry(self, pos):
        del self.entries[pos]

    def __str__(self):
        return '\n'.join(self.entries)
    
#    def save(self, filename):
#        file = open(filename, 'w')
#        file.write(str(self))
#        file.close()
#
#    def load(self, filename):
#        pass
#
#    def load_from_web(self, uri):
#        pass
#

class PersistenceManager:
    @staticmethod
    def save_to_file(journal, filename):
        file = open(filename, 'w')
        file.write(str(journal))
        file.close()

j = Journal()
j.add_entry('I cried today.')
j.add_entry('I read a book today.')
print(f'Journal entries:\n{j}')

file = '/tmp/journal.txt'
PersistenceManager.save_to_file(j, file)

with open(file) as fh:
    print(fh.read())
