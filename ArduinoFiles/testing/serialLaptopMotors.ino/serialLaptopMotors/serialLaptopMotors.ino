#include <Servo.h>

//Receiver arduino pins
const int pin4 = 6;
const int pin2 = 3;
//const int pin3 = 3;
const int pin5 = 5;
String inputString;

//Receiver channels
float channel4;
float channel2;
//float channel3;
float channel5;

//Servos and thrusters 
Servo servo;
//Servo servoLeft;
Servo thrusterRear;
//Servo thrusterRearLeft;
Servo thrusterFront;
//Servo thrusterFrontLeft;
 

void setup() {
  // put your setup code here, to run once:
  //Pin modes
  pinMode(pin4, INPUT);
  pinMode(pin2, INPUT);
  //pinMode(pin3, INPUT);
  pinMode(pin5, INPUT);
  servo.attach(9);
  //servoLeft.attach(7);
  thrusterRear.attach(10);
  //thrusterRearLeft.attach(11);
  thrusterFront.attach(11);
  //thrusterFrontLeft.attach(9);
  //Stop thrusters
  thrusterRear.writeMicroseconds(1500);
  //thrusterRearLeft.writeMicroseconds(1500);
  thrusterFront.writeMicroseconds(1500);
  //thrusterFrontLeft.writeMicroseconds(1500);
  //Driver setup
  delay(1000);
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
      //Serial.println("Autonomous");
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
        if(inputString[2] == 'x') {
        String valLeft = inputString.substring(4,8);
        Serial.println(valLeft);
        int angle = valLeft.toInt();
        servo.write(angle);
        //servoRight.write(angle); 
        }       
      }
      else if(inputString[0] == 'T') {
        //All thrusters 
        if(inputString[2] == 'a') {
          String valLeft = inputString.substring(4,8);
          //Serial.println(valLeft);
          int power = valLeft.toInt();
          thrusterRear.writeMicroseconds(power);
        }
        //Front Thrusters
        else if(inputString[2] == 'f') {
          String valLeft = inputString.substring(4,8);
          //Serial.println(valLeft);
          int power = valLeft.toInt();
          thrusterFront.writeMicroseconds(power);  
        }
        //back Thrusters
        else if(inputString[2] == 'b') {
          String valLeft = inputString.substring(4,8);
          //Serial.println(valLeft);
          int power = valLeft.toInt();
          thrusterFront.writeMicroseconds(power);
          //servoRight.write(angle); 
        }
        //Left thrusters
        else if(inputString[2] == 'l') {
          String valLeft = inputString.substring(4,8);
          //Serial.println(valLeft);
          int power = valLeft.toInt();
          thrusterFront.writeMicroseconds(power);
          //servoRight.write(angle); 
        }
        //Right thrusters
        else if(inputString[2] == 'r') {
          String valLeft = inputString.substring(4,8);
          //Serial.println(valLeft);
          int power = valLeft.toInt();
          thrusterFront.writeMicroseconds(power);
          //servoRight.write(angle); 
        }
        
        
      }

      //Delete Previous Message
      inputString = "";
    }
}
