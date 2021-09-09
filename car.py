import RPi.GPIO as GPIO
from time import sleep
import numpy as np


from l293d import L293d
from servo import Servo
from firebase import Firebase


class Car:
	
	def __init__(self, delay=0.3, deviation=0.015):
		self.delay = delay
		self.deviation = deviation

		self.l293d = L293d()
		self.servo = Servo()
		self.firebase = Firebase()

		sleep(0.5)
		self.max_volt = {}
		self.mid_volt = {}
		self.min_volt = {}
		
		self.mid_volt["up"], self.mid_volt["right"] = self.firebase.get_response() 
		if self.mid_volt["up"] == 0 or self.mid_volt["right"] == 0:
			raise Exception("voltage is 0")

		self.max_volt["up"] = self.mid_volt["up"] + 0.1
		self.max_volt["right"] = self.mid_volt["right"] + 0.1
		self.min_volt["up"] = self.mid_volt["up"] - 0.1
		self.min_volt["right"] = self.mid_volt["right"] - 0.1
		
	
	
	def translate_volt_to_portion(self, volt, axis):
		# axis is a boolean/int variable, if true/1 then use for up-down voltage, if false/0 use for right-left voltage
		# when the portion is reaching to the edge of the min/mid/max we will round it to this edge


		if abs(volt/self.mid_volt[axis]-1) < self.deviation:
			portion = 0

		elif volt > self.mid_volt[axis]:
			if self.max_volt[axis] < volt:
				self.max_volt[axis] = volt
			portion = (volt - self.mid_volt[axis])/(self.max_volt[axis]-self.mid_volt[axis])
			if portion > 1-self.deviation:
				portion = 1

		else: #if volt < self.mid_volt[axis]:
			if self.min_volt[axis] > volt:
				self.min_volt[axis] = volt
			portion = (volt - self.mid_volt[axis])/(self.mid_volt[axis] - self.min_volt[axis])
			if portion < -1+self.deviation:
				portion = -1    

		return portion
	
	
	def start(self):
		
		while True:
			up, right = self.firebase.get_response()
			up = self.translate_volt_to_portion(up, "up")
			right = self.translate_volt_to_portion(right, "right")
			self.servo.set_angle(right)
			self.l293d.set_speed(up)
			sleep(0.3)
		

	def test(self):
		while True:
			up, right = self.firebase.get_response()
			print("raw: up", up, "right", right)
			up = self.translate_volt_to_portion(up, "up")
			right = self.translate_volt_to_portion(right, "right")
			print("set: up", up, "right", right)
			self.servo.set_angle(right)
			self.l293d.set_speed(up)
		
    
if __name__ == "__main__":
      	
	
    try:
        c = Car()
        c.test()                                  

    except KeyboardInterrupt:
        print("Ctl C pressed - ending program")

    finally: 
        GPIO.cleanup()                          # resets GPIO ports used back to input mode

	
