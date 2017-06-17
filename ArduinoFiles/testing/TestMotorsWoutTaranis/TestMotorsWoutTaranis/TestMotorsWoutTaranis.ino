#include <Servo.h>

String inputString;

//Receiver channels
float channel4;
float channel2;
float channel5;

//Thrusters 
Servo thrusterRight;
Servo thrusterLeft;
 
String valLeft;

boolean autMode = false;

void setup() {
  //PIN Thrusters
  thrusterRight.attach(10);
  thrusterLeft.attach(11);

  //Stop thrusters
  thrusterRight.writeMicroseconds(1500);
  thrusterLeft.writeMicroseconds(1500);
  
  //Driver setup
  delay(1000);
  Serial.begin(115200);
}

void autonomous_Mode() {
  // put your main code here, to run repeatedly:
  while(!Serial.available()) {}
    // serial read section
    char c;
    
    while (Serial.available() > 0) {
        char c = Serial.read();
        inputString += c;  
        //wait for the next byte, if after this nothing has arrived it means 
        //the text was not part of the same stream entered by the user
        delay(1); 
    }
    
  //0123456789012
  //%B,1500,1500%
    if(inputString[0] == '%' && inputString.length() > 0 && inputString.length() < 14 && inputString[inputString.length() - 1] == '%' && inputString != ""){
      //Serial.println(inputString);
      if(inputString[1] == 'B') {
          String valRight = inputString.substring(3,7);
          String valLeft = inputString.substring(8,12);
          //Serial.println(valLeft);
          int powerL = valLeft.toInt();
          int powerR = valRight.toInt();
          
          thrusterRight.writeMicroseconds(powerR);
          //Serial.print(powerR);
          thrusterLeft.writeMicroseconds(powerL);
          //Serial.println(powerL);
        }
        //Left thrusters
        else if(inputString[1] == 'L') {
          String valLeft = inputString.substring(3,7);
          //Serial.println(valLeft);
          int power = valLeft.toInt();
          thrusterLeft.writeMicroseconds(power); 
          Serial.print(power);
        }
        //Right thrusters
        else if(inputString[1] == 'R') {
          String valRight = inputString.substring(3,7);
          //Serial.println(valRight);
          int power = valRight.toInt();
          thrusterRight.writeMicroseconds(power);
          Serial.print(power);
          //servoRight.write(angle); 
        }
    }  
    //Delete Previous Message
     inputString = "";

}
void loop() {
  autonomous_Mode();
}
