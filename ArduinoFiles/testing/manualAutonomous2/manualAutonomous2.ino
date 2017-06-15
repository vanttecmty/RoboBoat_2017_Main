#include <Servo.h>

//Receiver arduino pins
const int pin4 = 6;
const int pin2 = 3;
//const int pin3 = 3;
const int pin5 = 2;
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

void read_values () {
  //Read channel frequecies
  channel4 = pulseIn(pin4, HIGH);
  channel2 = pulseIn(pin2, HIGH);
  //channel3 = pulseIn(pin3, HIGH);
  channel5 = pulseIn(pin5, HIGH);
}

void select(){
  //Use channel 5 to select current mode
  if (channel5 > 1600){
    move_2();
    Serial.print("m");
  }
  else if (channel5 < 1400){
    power_Difference();
    Serial.print("pd");
  }
  else{
    autonomous_Mode();
    Serial.print("a");
  }
}

void move_2 (){ //Remote control movement
  if (channel4 > 1470 & channel4 < 1530){
    //Servos at the middle
    servo.write(90);
    //servoLeft.write(90);
  }
  else {
    //Servo movement relation
    servo.write(map(channel4, 2000, 950, 0, 180));
    //servoLeft.write(map(channel4, 2000, 950, 0, 180));
  }
  if (channel2 > 1470 & channel2 < 1530) {
    //Range to stop thrusters
    thrusterFront.writeMicroseconds(1500);
    //thrusterFrontLeft.writeMicroseconds(1500);
    thrusterRear.writeMicroseconds(1500);
    //thrusterRearLeft.writeMicroseconds(1500);
  }
  else {
    //Thrusters signal
    thrusterFront.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
    //thrusterFrontLeft.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
    thrusterRear.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
    //thrusterRearLeft.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));

  }
}

void power_Difference(){
  float y;
  float R;
  float L;
  if ((channel4 > 1470 & channel4 < 1515) & (channel2 > 1470 & channel2 < 1515)){
    thrusterRear.writeMicroseconds(1500);
    //thrusterRearLeft.writeMicroseconds(1500);
    thrusterFront.writeMicroseconds(1500);
    //thrusterFrontLeft.writeMicroseconds(1500);
  }
  else if ((channel4 > 1470 & channel4 < 1515) & (channel2 < 1470 || channel2 > 1515)) {
    thrusterRear.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
    //thrusterRearLeft.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
    thrusterFront.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
    //thrusterFrontLeft.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
  }
  else if ((channel4 < 1470 || channel4 > 1515) & (channel2 > 1470 & channel2 < 1515)) {
    R=map(channel4, 975, 2025, 1900, 1100);
    L=map(channel4, 975, 2025, 1100, 1900);
    thrusterRear.writeMicroseconds(R);
    //thrusterRearLeft.writeMicroseconds(L);
    thrusterFront.writeMicroseconds(R);
    //thrusterFrontLeft.writeMicroseconds(L);
  }
  else if ((channel4 < 1470) & (channel2 < 1470 || channel2 > 1515)) {
    y = (channel2-(channel2-1500)*(1500-channel4)/525);
    R=map(channel2, 975, 2025, 1100, 1900);
    L=map(y, 975, 2025, 1100, 1900);
    thrusterRear.writeMicroseconds(R);
    //thrusterRearLeft.writeMicroseconds(L);
    thrusterFront.writeMicroseconds(R);
    //thrusterFrontLeft.writeMicroseconds(L);
  }
  else if ((channel4 > 1515) & (channel2 < 1470 || channel2 > 1515)) {
    y = (channel2-(channel2-1500)*(channel4-1500)/525);
    R=map(y, 975, 2025, 1100, 1900);
    L=map(channel2, 975, 2025, 1100, 1900);
    thrusterRear.writeMicroseconds(R);
    //thrusterRearLeft.writeMicroseconds(L);
    thrusterFront.writeMicroseconds(R);
    //thrusterFrontLeft.writeMicroseconds(L);
  }
}

void autonomous_Mode(){
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
      //Serial.println(inputString);
      //digitalWrite(LED_BUILTIN, HIGH);
      if(inputString[0] == 'S') {
        if(inputString[2] == 'x') {
        String valLeft = inputString.substring(4,8);
        //Serial.println(valLeft);
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

void loop() {
  read_values();
  select();
}
