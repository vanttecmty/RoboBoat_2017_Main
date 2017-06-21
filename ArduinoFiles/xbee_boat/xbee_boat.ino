#include <SoftwareSerial.h>
#define pinRX 2
#define pinTX 3
SoftwareSerial XBee(pinRX, pinTX);
int ledM1 = 13;
String incomingByte;
String message;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  XBee.begin(9600);
}

void loop() {
  // send with xbee when received from pc
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.readString();
    int strlength = incomingByte.length();

    for(int i=0;i<=strlength;i++) {
      XBee.write(incomingByte[i]);
    }
  }

  while(XBee.available() > 0) {
    char dato;
    dato = (char) XBee.read();

    //Serial.println(dato);
    message+=dato;
  }

  if(message.length() > 0 && message[message.length() - 1] == '%') {
    Serial.println(message);
    message = "";
  }
}