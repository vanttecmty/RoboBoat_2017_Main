#include <SoftwareSerial.h>
#define pinRX 2
#define pinTX 3
SoftwareSerial XBee(pinRX,pinTX);

int led = 13; //Led indicador de encendido de la alarma
String inputString = "";

void setup() {
  Serial.begin(9600); //Comunicacion serial con processing
  XBee.begin(9600);
  pinMode(led, OUTPUT);
}

void loop() {
  //XBee.write("Hola Mundo");
  if(XBee.available() > 0) {
      char dato;
      dato = (char) XBee.read();
      inputString.concat(dato);   
  }
  
  Serial.println(inputString);
}
