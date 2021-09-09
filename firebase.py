import requests
import json
from time import sleep

class Firebase:
        
    project_name = "https://rasperry-1996-default-rtdb.firebaseio.com"
    path = "/remote_control_car/joystick"
    url = project_name + path + "/.json"
    
    def __init__(self):
        pass
        
    # get data from firebase
    def get_response(self):
        response = None
        while response is None:
            response = self.get()
            
        return response
        
    
    def get(self):
        try:
            response = requests.get(Firebase.url).json()
            print(response)
            return response["up"], response["right"]
            
        except Exception as e:
            print("error while GET:")
            print("error: ", e)


    # patch data to firebase
    def patch(self):
        try:
            values = {"key":{
                "key1": "value1",
                "key2": "value2"
                }}
            data = json.dumps(values)
            response = requests.patch(Firebase.url, data)
            print(response)
        except Exception as e:
            print("error while PATCH:")
            print("data: ", data)
            print("error: ", e)
        

    # delete data
    def delete(self):
        try:
            response = requests.delete(Firebase.url)
            print(response)
        except Exception as e:
            print("error while DELETE:")
            print("error: ", e)
            
if __name__ == "__main__":
    fb = Firebase()
    while 1:
        fb.get_response()
        sleep(1)
        
