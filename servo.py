import RPi.GPIO as GPIO
from time import sleep
import numpy as np


"""
pwm - pin 8
freq = 50KHz
duty cylcle is 2% - 11.3% 
angle is -90 to +90

"""

class Servo:
        max_right = 11.2  # 90 degrees
        max_left = 2 # -90 degrees
	end_duty_cycle = max_right - (max_right - max_left)/4.5     
	start_duty_cycle = max_left + (max_right - max_left)/4.5
    
	middle_duty_cycle = (start_duty_cycle + end_duty_cycle) / 2
	
	start_angle = -1
	end_angle = 1
	middle_angle = (start_angle + end_angle) / 2
	step = (end_angle - start_angle)/30.0
	
	
	

	def __init__(self, pwm_pin=10, khz=50):
		# GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)

		GPIO.setup(pwm_pin, GPIO.OUT) 
		self.pwm = GPIO.PWM(pwm_pin, khz)  
		self.angle= Servo.middle_angle                                
		self.pwm.start(Servo.angle_to_dc(self.angle))  
		sleep(0.5)

                    

	@staticmethod
	def angle_to_dc(angle):
		#     
                dc = (angle - Servo.start_angle)*(Servo.end_duty_cycle-Servo.start_duty_cycle)/(Servo.end_angle-Servo.start_angle) + Servo.start_duty_cycle
		return dc


	def set_angle(self, new_angle, smooth=True):
		if smooth:
			step_direction = 1 if self.angle <= new_angle else -1
			for i in np.arange(self.angle, new_angle+Servo.step*step_direction, Servo.step*step_direction):
				self.pwm.ChangeDutyCycle(Servo.angle_to_dc(i)) 
				sleep(0.02)      
			
			self.angle = new_angle

		else:
			self.angle = new_angle
			self.pwm.ChangeDutyCycle(Servo.angle_to_dc(new_angle))  
			sleep(0.2)      
			
		self.pwm.ChangeDutyCycle(0)      

	def stop(self):
		self.dc = Servo.middle_duty_cycle;
		

def calibrate_servo():
	  p = Servo()
	  p.pwm.ChangeDutyCycle(Servo.middle_duty_cycle)    
	  sleep(5)   
	  p.pwm.ChangeDutyCycle(Servo.start_duty_cycle)    
	  sleep(5)   
	  p.pwm.ChangeDutyCycle(Servo.end_duty_cycle)   
	  sleep(5)  
	

    
if __name__ == "__main__":
		  
	try:
		  p = Servo()
		  sleep(2)     
		  print(-1)        
		  p.set_angle(-1)   
		  sleep(2)         
		  print(0)        
		  p.set_angle(0)  
		  sleep(2)         
		  print(1)        
		  p.set_angle(1) 
		  sleep(2)    
		  
		  print(0.75)
		  p.set_angle(0.75, False) 
		  sleep(2)       
		  print(--0.3)          
		  p.set_angle(-0.3, False) 
		  sleep(2)      
		  
		  #p.stop()      
		  
		  
	except KeyboardInterrupt:
		print("Ctl C pressed - ending program")

	finally: 
	  # p.pwm.stop()                         # stop PWM
	  GPIO.cleanup()  
