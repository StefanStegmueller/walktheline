class AutoController:

  def __init__(self):
    self.Ta = 0.09     #Abstastzeit
    self.max = 1.0
    self.min = -1.0
    self.Kp = 1.5    #1.5
    self.Ki = 0.2   #0.2
    self.Kd = self.Ki * 0.1
    self.pre_error = 0.0
    self.integral = 0.0

  
  def controll_direction(self, positionOfTheLine):
    setpoint = 0.0
    
    # Calculate error
    error = setpoint + positionOfTheLine
    
    # P
    Pout = self.Kp * error
    print '$$$$$$$$$$$$$ Pout: ' + str(Pout)
    
    # I
    self.integral += error * self.Ta;
    Iout = self.Ki * self.integral;
    print '$$$$$$$$$$$$$ Iout: ' + str(Iout)
    
    # D
    derivative = (self.pre_error - error) / self.Ta;
    Dout = self.Kd * derivative;
    print '$$$$$$$$$$$$$ Dout: ' + str(Dout)
    
    
    # output
    output = Pout + Iout + Dout
    print '$$$$$$$$$$$$$ output: ' + str(output)
    
    if output > self.max:
      output = self.max
    elif output < self.min:
      output = self.min
    
  
    # Save error to previous error
    self.pre_error = error;

    return output;
