#include <SoftwareSerial.h>

//XBee program
#define pinRX 2
#define pinTX 3

//Turnigy Kill Switch variables
#define V8FR_PIN_7 7
#define V8FR_PIN_8 8
#define V8FR_PIN_9 9
#define V8FR_PIN_10 10
#define Kill_PIN_12 12

float channel7;
float channel6;

int n = 0;
int m = 0;

String incomingByte;
String message;

boolean received;

SoftwareSerial XBee(pinRX, pinTX);

void setup() {
  // XBee initializations
  Serial.begin(9600);
  XBee.begin(9600);

  //Emergency and landing Kill switch pins
  pinMode(V8FR_PIN_7, OUTPUT);
  pinMode(V8FR_PIN_8, OUTPUT);
  pinMode(Kill_PIN_12, OUTPUT);
  pinMode(V8FR_PIN_9, INPUT);
  pinMode(V8FR_PIN_10, INPUT);
}

void read_values(){
  //read RC channel Frequencies
  channel6 = pulseIn(V8FR_PIN_9,HIGH);
  //channel7 = pulseIn(V8FR_PIN_10,HIGH);
}

void emergency_landing(){
  //Send emergency string to app
  Serial.print("emergency%");
}

void boat_kill_Switch(){
  //Send emergency string to app
  digitalWrite(Kill_PIN_12, HIGH);
}

void counters(){
  //Counter for emergency landing switch
  if(channel7 < 1400){
    n = n + 1;
  }
  else{
    n = 0;
  }

  //Counter kill switch
  if(channel6 > 1700){
    m = m + 1;
  }
  else{
    m = 0;
  }
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
  //End of Xbee segment

  //
  
  read_values();
  /*
  counters();
  if (received){
    int strlength = message.length();
    for (int i = 0; i <= strlength; ++i){
      Serial.write(message[i]);
    }
  }
  if (m > 2000){
    boat_kill_Switch();
  }
  if (n > 2000){
    emergency_landing();
  }
  */
}
