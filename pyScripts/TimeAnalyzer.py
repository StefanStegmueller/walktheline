import time

class TimeAnalyzer:

    def __init__(self, name):
        self.__startDate = 0
        self.__name = name
        self.__iteration = 0

    def start(self):
        self.__startDate = time.time()

    def stop(self):
        duration = time.time() - self.__startDate
        print "(" + str(self.__iteration) + ") Duration for " + self.__name + ": " + str(duration)
        self.__iteration += 1

