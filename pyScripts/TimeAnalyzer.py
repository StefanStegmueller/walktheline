import time

class TimeAnalyzer:

    def __init__(self, name):
	self.startDate = 0
        self.name = name
        self.iteration = 0

    def start(self):
        self.startDate = time.time()

    def stop(self):
        duration = time.time() - self.startDate
        print "(" + str(self.iteration) + ") Duration for " + self.name + ": " + str(duration)
        self.iteration += 1

