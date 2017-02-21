import time

class TimeAnalyzer:

    def __init__(self, name):
        self.start = 0
        self.name = name
        self.iteration = 0

    def start(self):
        self.start = time.time()

    def stop(self):
        duration = time.time() - start
        print "(" + str(self.iteration) + ") Duration for " + self.name + ": " + duration
        self.iteration += 1

