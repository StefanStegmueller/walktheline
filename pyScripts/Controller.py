class Controller(object):
  
  def __init__(self):
    self.lastInputs = [3]
    self.lastInputs.append(0.0) # e(k-2)
    self.lastInputs.append(0.0) # e(k-1)
    self.lastInputs.append(0.0) # e(k)
    self.lastOutputs = [2]
    self.lastOutputs.append(0.0)  # u(k-2)
    self.lastOutputs.append(0.0)  # u(k-1)
  
  
  
  
  def controllDirection(self, positionOfTheLine):
    #u(k) = p2*u(k-2) + p1*u(k-1) + q0*e(k) + q1*e(k-1) + q2*e(k-2)
    
    Kp = 0.1
    Ki = 1
    Kd = 0.0005
    Ta = 0.1
    Ti = 0.05 # Nachstellzeit
    Td = 0.01 # Vorstellzeit
    
    p2 = 0.2
    p1 = 0.05
    
    q0 = Kp + Ki * Ta/2 * Ti + Kd * Td/Ta
    q1 = -Kp + Ki * Ta/2 * Ti - Kd*2*Td/Ta
    q2 = Kd*Td/Ta
    
    
    self.addInput(positionOfTheLine)
    
    output = p2*self.lastOutputs[0] + p1 * self.lastOutputs[1] + q0 * self.lastInputs[2] + q1 * self.lastInputs[1] + q2 * self.lastInputs[0]
    
    self.addOutput(output)


    return output
    
    
  def addInput(self, positionOfTheLine):
    self.lastInputs[0] = self.lastInputs[1]
    self.lastInputs[1] = self.lastInputs[2]
    self.lastInputs[2] = positionOfTheLine
    return
  
  def addOutput(self, output):
    self.lastOutputs[0] = self.lastOutputs[1]
    self.lastOutputs[1] = output
    return
