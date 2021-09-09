import RPi.GPIO as GPIO
from time import sleep


"""
connections 
            L293D

 3        pwm1  5v      2
 5        dir1  dir2
 motor    out1  out2
 battery  gnd   gnd     6
          gnd   gnd
 motor    out1  out2  
 11       dir1  dir2
 battery  v-in  pwm2
"""



class L293d:
  
  
  start_portion = -1
  end_portion = 1
  middle_portion = (start_portion + end_portion) / 2

  def __init__(self, pwm_pin=3, dir1_pin=5, dir2_pin=11, khz=9):
    # GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    self.dir_pin1 = dir1_pin
    GPIO.setup(self.dir_pin1,GPIO.OUT)
    GPIO.output(self.dir_pin1, 1)

    self.dir_pin2 = dir2_pin
    GPIO.setup(self.dir_pin2,GPIO.OUT)
    GPIO.output(self.dir_pin2, 0)

    GPIO.setup(pwm_pin, GPIO.OUT) 
    self.pwm = GPIO.PWM(pwm_pin, khz)  
    self.dc=0            # duty cycle                          
    self.pwm.start(self.dc)  
        
    self.dir_value = 1

    
  def set_dirction(self, dirction='switch'):
    if dirction == 'switch':
      self.dir_value = not self.dir_value
    elif dirction == "forword":
      self.dir_value = True
    elif dirction == "backward":
      self.dir_value = False
    else:
      raise Exeption("dirction is not recocnize, value:", dirction)
      
    GPIO.output(self.dir_pin1, self.dir_value)
    GPIO.output(self.dir_pin2, not self.dir_value)

  def set_dc(self, portion):
    new_dc = abs(portion - L293d.middle_portion)*100*2/(L293d.end_portion - L293d.start_portion)
    self.pwm.ChangeDutyCycle(new_dc)  
  
  def stop(self):
    self.dir_value = False
    GPIO.output(self.dir_pin1, self.dir_value)
    GPIO.output(self.dir_pin2, self.dir_value)
    
  def set_speed(self, portion):
    if portion > L293d.middle_portion:
      self.set_dirction("forword")
    elif portion < L293d.middle_portion:
      self.set_dirction("backward")
      
    self.set_dc(portion)
      
    
    
    
if __name__ == "__main__":
      
  try:
    GPIO.cleanup()
    p = L293d()
    # p.test()
    sleep(2)             
    p.set_dc(50) 
    sleep(2)        
    p.set_dirction()  
    sleep(2)            
    p.set_dc(100) 
    sleep(2)        
    p.set_dirction('forword')    
    sleep(2)                 
    p.set_dc(20) 
    sleep(2)        
    p.set_dirction('backward')  
    sleep(2)                  
    p.stop() 
    sleep(2)                                      
    
  except KeyboardInterrupt:
    print("Ctl C pressed - ending program")
    
  finally: 
    # p.pwm.stop()                         # stop PWM
    GPIO.cleanup()                          # resets GPIO ports used back to input mode

