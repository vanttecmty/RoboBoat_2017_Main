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
    while (Serial.available()) {
      if (Serial.available() >0) {
        char c = Serial.read();
        inputString += c;  
      }
    }

    //Send String received to confirm it was correctly received
    Serial.print(inputString);
    Serial.flush();
    
    if(inputString.length() == 1){
      if(inputString[0] == 'S'){
        //Serial.print("InS");
        if(inputString[2] == 'b'){
          //Serial.print("InB");
          String valLeft = inputString.substring(4,7);
          String valRight = inputString.substring(8,11);
          //servoLeft.write(valLeft.toInt());
          //servoRight.write(valRight.toInt());        
        }
        //else{
          //Serial.print("ElB");
        //}
      }//else{
        //Serial.print("ElS");
      //}
    }
    //else{
      //Serial.print("123"); 
      //Serial.print("456");
    //}
    Serial.flush();
    //Delete Previous Message
    inputString = "";
}
