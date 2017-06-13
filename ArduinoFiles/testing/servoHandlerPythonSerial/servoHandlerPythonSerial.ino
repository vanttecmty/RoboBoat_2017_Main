//#include <VirtualWire.h>
#include <Servo.h>

char inData[256];
int setPoint = 55;
String inputString;
Servo servoLeft;
Servo servoRight;

int pinServoLeft = 7;
int pinServoRight = 6;

//'S,b,0180%'

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
    char c;
    while (Serial.available() > 0) {
        char c = Serial.read();
        inputString += c;  
        //wait for the next byte, if after this nothing has arrived it means 
        //the text was not part of the same stream entered by the user
        delay(1); 
    }

    if(inputString.length() > 0 && inputString[inputString.length() - 1] == '%'){
      Serial.println(inputString);
      //digitalWrite(LED_BUILTIN, HIGH);
      if(inputString[0] == 'S') {
        String valLeft = inputString.substring(2,6);
        int angle = valLeft.toInt();
        servoLeft.write(angle);
        servoRight.write(angle);        
      }
      else if(inputString[0] == 'T') {
        String valLeft = inputString.substring(2,6);
        int angle = valLeft.toInt();
        servoLeft.write(angle);
        servoRight.write(angle);        
      }

      //Delete Previous Message
      inputString = "";
    }
}
