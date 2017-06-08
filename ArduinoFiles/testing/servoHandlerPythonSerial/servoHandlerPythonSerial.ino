//#include <VirtualWire.h>
#include <Servo.h>

char inData[256];
int setPoint = 55;
String readString;
Servo servoLeft;
Servo servoRight;

int pinServoLeft = 10;
int pinServoRight = 11;

void setup()
{
  //Declare servos
  servoLeft.attach(pinServoLeft);
  servoRight.attach(pinServoRight);
  
  pinMode(LED_BUILTIN, OUTPUT);
  //Initialize Serial communication at 9600 bps
  Serial.begin(9600);  
}

void loop(){
    while(!Serial.available()) {}

    //digitalWrite(LED_BUILTIN, HIGH);
    // serial read section
    while (Serial.available()) {
      if (Serial.available() >0) {
        char c = Serial.read();
        readString += c;  
      }
    }
    
    if (readString.length() == 11){
       //Serial.print(readString);
       //Serial.print(readString[0]);
       if(readString[0] == 'S'){
          if(readString[2] == 'b'){
            String valLeft = readString.substring(4,7);
            String valRight = readString.substring(8,11);
            servoLeft.write(valLeft.toInt());
            servoRight.write(valRight.toInt());        
          }
       }
      Serial.flush();
      //Delete Previous Message
      readString = "";
    }

}
