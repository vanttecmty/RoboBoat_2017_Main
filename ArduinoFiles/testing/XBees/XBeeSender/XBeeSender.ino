#include <SoftwareSerial.h>
#define pinRX 0
#define pinTX 1
SoftwareSerial XBee(pinRX,pinTX);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  XBee.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  char buff[100]; 
  String val = Serial.readString();
  for(int i = 0; i < val.length(); i++){
    XBee.write(val[i]);
  }
}
