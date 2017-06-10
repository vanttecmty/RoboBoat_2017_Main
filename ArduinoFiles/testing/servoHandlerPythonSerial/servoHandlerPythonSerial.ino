//#include <VirtualWire.h>
#include <Servo.h>

char inData[256];
int setPoint = 55;
String inputString;
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
    char c;
    while (Serial.available() > 0) {
        char c = Serial.read();
        inputString += c;  
        //wait for the next byte, if after this nothing has arrived it means 
        //the text was not part of the same stream entered by the user
        delay(1); 
        //Serial.println(c);
    }

    
      //Send String received to confirm it was correctly received4
      //Serial.println(inputString);
      //Serial.flush();
      //Serial.println(inputString.length());
      //Serial.flush();
      //inputString = "";
     
    
    if(inputString.length() > 0 && inputString[inputString.length() - 1] == '%'){
      //digitalWrite(LED_BUILTIN, HIGH);
      if(inputString[0] == 'S') {
        //Serial.print("InS");
        if(inputString[2] == 'b'){
          //Serial.print("InB");
          String valLeft = inputString.substring(4,7);
          String valRight = inputString.substring(8,11);
          Serial.print(valLeft + valRight);
          servoLeft.write(valLeft.toInt());
          servoRight.write(valRight.toInt());        
        }
      }

      //Delete Previous Message
      inputString = "";
      Serial.flush();
    } else {
      digitalWrite(LED_BUILTIN, HIGH);
      //Serial.println(inputString.length());
    }
}
