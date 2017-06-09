#include <Servo.h>

char inData[256];
int setPoint = 55;
String inString;
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
    int counter = 0;
    while(!Serial.available()) {}

    //digitalWrite(LED_BUILTIN, HIGH);
    // serial read section
    while (Serial.available()) {
        char c = '\0';
        if(c = Serial.read() == 'S') {
          counter ++;
          while(counter <= 11){
            inString += c;  
            c = Serial.read();
            counter++;
          }
        }
    }
    
    Serial.print(inString);
    /*
    if (inString.length() >= 11){
       if(inString[0] == 'S'){
          if(inString[2] == 'b'){ 
            String valLeft = inString.substring(4,7);
            String valRight = inString.substring(8,11);
            //Serial.print(valLeft + valRight);
            //servoLeft.write(valLeft.toInt());
            //servoRight.write(valRight.toInt());        
          }
       }
      Serial.flush();
      //Delete Previous Message
      inString = "";
    }*/
}
