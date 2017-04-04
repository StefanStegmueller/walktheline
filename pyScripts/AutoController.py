class AutoController:

  def __init__(self):
    self.__ta = 0.09     #Abstastzeit
    self.__max = 1.0
    self.__min = -1.0
    self.__kp = 1.5    #1.5
    self.__ki = 0.2   #0.2
    self.__kd = self.__ki * 0.1
    self.__pre_error = 0.0
    self.__integral = 0.0

  
  def controll_direction(self, positionOfTheLine):
    setpoint = 0.0
    
    # Calculate error
    error = setpoint + positionOfTheLine
    
    # P
    Pout = self.__kp * error
    print '$$$$$$$$$$$$$ Pout: ' + str(Pout)
    
    # I
    self.__integral += error * self.__ta;
    Iout = self.__ki * self.__integral;
    print '$$$$$$$$$$$$$ Iout: ' + str(Iout)
    
    # D
    derivative = (self.__pre_error - error) / self.__ta;
    Dout = self.__kd * derivative;
    print '$$$$$$$$$$$$$ Dout: ' + str(Dout)
    
    
    # output
    output = Pout + Iout + Dout
    print '$$$$$$$$$$$$$ output: ' + str(output)
    
    if output > self.__max:
      output = self.__max
    elif output < self.__min:
      output = self.__min
    
  
    # Save error to previous error
    self.__pre_error = error;

    return output;
