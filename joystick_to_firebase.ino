/***************************************************
Simple example of reading the MCP3008 analog input channels and printing
them all out.
Author: Carter Nelson
License: Public Domain
****************************************************/

#include <Adafruit_MCP3008.h>
Adafruit_MCP3008 adc;
int SSPin = 2;
int channels[] = {0,1};
float data[] = {-1,-1};



#include "FirebaseESP8266.h"  // Install Firebase ESP8266 library
#include <ESP8266WiFi.h>
#define FIREBASE_HOST "rasperry-1996-default-rtdb.firebaseio.com" 
#define FIREBASE_AUTH "JQ4yVkaPjGkykkRIHddPrH651Jn4KWwYL0M9P27M"


#define WIFI_SSID "Oria" // "Oren_2.4G"  //"toledano"
#define WIFI_PASSWORD "0542405993"  // "12qwaszx"    //"toledano3"

int led = 0;     // Connect LED to D5

//Define FirebaseESP8266 data object
FirebaseData firebaseData;
FirebaseData ledData;


/* joystick    MSP3008    feather             feather
 *             
 * up/down    CH0  Vdd    3.3V            
 * right/left CH1  Vref   3.3V        
 *            CH2  Agnd   
 *            CH3  CLK    P14
 *            CH4  Dout   P12
 *            CH5  Din    P13
 *            CH6  CS     P15
 *            CH7  Dgnd   
 * 
 */


void setup() {
  Serial.begin(9600);
  while (!Serial);

  adc.begin(14,13,12,15);
  //       (sck, mosi, miso, cs)


  
  pinMode(led,OUTPUT);
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);

  
}

void loop() {
  
  for (int i=0; i<(sizeof(channels)/sizeof(int)); i++) {
    data[i] = adc.readADC(channels[i])/1023.0;
    Serial.print(data[i]); Serial.print("\t");
  }
  Serial.print("\n\n");

 
  String firebase_post_path = "/remote_control_car/joystick";
  // send POST request with the value in var t to firebase_

  // other options other then set float are: 
  // set, setInt, setFloat, setDouble, setBool, setString, setJSON, setArray, setBlob and setFile
  if (Firebase.setFloat(firebaseData, firebase_post_path+"/up", data[0]) && Firebase.setFloat(firebaseData, firebase_post_path+"/right", data[1]))
  {
    // print data into the com serial monitor
    Serial.println("PASSED");
  }
  else
  {
    Serial.println("FAILED");
    Serial.println("REASON: " + firebaseData.errorReason());
  }

}
