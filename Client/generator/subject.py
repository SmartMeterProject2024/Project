# Observer Pattern
class Subject:
    def __init__(self):
        self._observers = [] # initialise with 0 observers watching

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, interval, usage):
        for observer in self._observers:
            observer.update(interval, usage) # updates all observers