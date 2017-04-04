import SettingsParser

class AutoController:

  def __init__(self):
    self.__ta = SettingsParser.get_value("controller", "ta")   #Abstastzeit
    self.__max = SettingsParser.get_value("controller", "min")
    self.__min = SettingsParser.get_value("controller", "max")
    self.__kp = SettingsParser.get_value("controller", "kp")
    self.__ki = SettingsParser.get_value("controller", "ki")
    self.__kd = self.__ki * SettingsParser.get_value("controller", "kd_factor")
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
