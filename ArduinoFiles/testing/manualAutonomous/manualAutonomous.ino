#include <Servo.h>

String inputString = "";
//Receiver arduino pins
const int pin4 = 4;
const int pin2 = 2;
const int pin3 = 3;
const int pin5 = 5;

//Receiver channels
float channel4;
float channel2;
float channel3;
float channel5;

//Servos and thrusters 
Servo servoRight;
Servo servoLeft;
Servo thrusterRearRight;
Servo thrusterRearLeft;
Servo thrusterFrontRight;
Servo thrusterFrontLeft;
 
void setup() {
  //Pin modes
  pinMode(pin4, INPUT);
  pinMode(pin2, INPUT);
  pinMode(pin3, INPUT);
  pinMode(pin5, INPUT);
  servoRight.attach(6);
  servoLeft.attach(7);
  thrusterRearRight.attach(10);
  thrusterRearLeft.attach(11);
  thrusterFrontRight.attach(8);
  thrusterFrontLeft.attach(9);
  //Stop thrusters
  thrusterRearRight.writeMicroseconds(1500);
  thrusterRearLeft.writeMicroseconds(1500);
  thrusterFrontRight.writeMicroseconds(1500);
  thrusterFrontLeft.writeMicroseconds(1500);
  //Driver setup
  delay(1000);
  Serial.begin(9600);
}

void read_values () {
  //Read channel frequecies
  channel4 = pulseIn(pin4, HIGH);
  channel2 = pulseIn(pin2, HIGH);
  channel3 = pulseIn(pin3, HIGH);
  channel5 = pulseIn(pin5, HIGH);
}

void select(){
  //Use channel 5 to select current mode
  if (channel5 > 1600){
    move_2();
  }
  else if (channel5 < 1400){
    power_Difference();
  }
  else{
    autonomous_Mode();
  }
}

void move_1 (){ //Remote control movement
  if (channel4 > 1470 & channel4 < 1530){
    //Servos at the middle
    servoRight.write(90);
    servoLeft.write(90);
  }
  else {
    //Servo movement relation
    servoRight.write(map(channel4, 2000, 950, 0, 180));
    servoLeft.write(map(channel4, 2000, 950, 0, 180));
  }
  if (channel3 > 1470 & channel3 < 1530) {
    //Range to stop rear thrusters
    thrusterRearRight.writeMicroseconds(1500);
    thrusterRearLeft.writeMicroseconds(1500);
  }
  else {
    //Rear thrusters signal
    thrusterRearRight.writeMicroseconds(map(channel3, 988, 2012, 1100, 1900));
    thrusterRearLeft.writeMicroseconds(map(channel3, 988, 2012, 1100, 1900));
  }
  if (channel2 > 1470 & channel2 < 1530) {
    //Range to stop front thrusters
    thrusterFrontRight.writeMicroseconds(1500);
    thrusterFrontLeft.writeMicroseconds(1500);
  }
  else {
    //Front thrusters signal
    thrusterFrontRight.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
    thrusterFrontLeft.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
  }
}

void move_2 (){ //Remote control movement
  if (channel4 > 1470 & channel4 < 1530){
    //Servos at the middle
    servoRight.write(90);
    servoLeft.write(90);
  }
  else {
    //Servo movement relation
    servoRight.write(map(channel4, 2000, 950, 0, 180));
    servoLeft.write(map(channel4, 2000, 950, 0, 180));
  }
  if (channel2 > 1470 & channel2 < 1530) {
    //Range to stop thrusters
    thrusterFrontRight.writeMicroseconds(1500);
    thrusterFrontLeft.writeMicroseconds(1500);
    thrusterRearRight.writeMicroseconds(1500);
    thrusterRearLeft.writeMicroseconds(1500);
  }
  else {
    //Thrusters signal
    thrusterFrontRight.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
    thrusterFrontLeft.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
    thrusterRearRight.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
    thrusterRearLeft.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));

  }
}

void power_Difference(){
  float y;
  float R;
  float L;
  if ((channel4 > 1470 & channel4 < 1515) & (channel2 > 1470 & channel2 < 1515)){
    thrusterRearRight.writeMicroseconds(1500);
    thrusterRearLeft.writeMicroseconds(1500);
    thrusterFrontRight.writeMicroseconds(1500);
    thrusterFrontLeft.writeMicroseconds(1500);
  }
  else if ((channel4 > 1470 & channel4 < 1515) & (channel2 < 1470 || channel2 > 1515)) {
    thrusterRearRight.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
    thrusterRearLeft.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
    thrusterFrontRight.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
    thrusterFrontLeft.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
  }
  else if ((channel4 < 1470 || channel4 > 1515) & (channel2 > 1470 & channel2 < 1515)) {
    R=map(channel4, 975, 2025, 1900, 1100);
    L=map(channel4, 975, 2025, 1100, 1900);
    thrusterRearRight.writeMicroseconds(R);
    thrusterRearLeft.writeMicroseconds(L);
    thrusterFrontRight.writeMicroseconds(R);
    thrusterFrontLeft.writeMicroseconds(L);
  }
  else if ((channel4 < 1470) & (channel2 < 1470 || channel2 > 1515)) {
    y = (channel2-(channel2-1500)*(1500-channel4)/525);
    R=map(channel2, 975, 2025, 1100, 1900);
    L=map(y, 975, 2025, 1100, 1900);
    thrusterRearRight.writeMicroseconds(R);
    thrusterRearLeft.writeMicroseconds(L);
    thrusterFrontRight.writeMicroseconds(R);
    thrusterFrontLeft.writeMicroseconds(L);
  }
  else if ((channel4 > 1515) & (channel2 < 1470 || channel2 > 1515)) {
    y = (channel2-(channel2-1500)*(channel4-1500)/525);
    R=map(y, 975, 2025, 1100, 1900);
    L=map(channel2, 975, 2025, 1100, 1900);
    thrusterRearRight.writeMicroseconds(R);
    thrusterRearLeft.writeMicroseconds(L);
    thrusterFrontRight.writeMicroseconds(R);
    thrusterFrontLeft.writeMicroseconds(L);
  }
}

void autonomous_Mode(){
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
        Serial.println(valLeft);
        int angle = valLeft.toInt();
        servoLeft.write(angle);
        servoRight.write(angle);
        }       
      }
      else if(inputString[0] == 'T') {
        if(inputString[2] == 'b') {
          String valLeft = inputString.substring(4,8);
          Serial.println(valLeft);
          int power = valLeft.toInt();
          thrusterRear.writeMicroseconds(power);
        }else if(inputString[2] == 'f') {
          String valLeft = inputString.substring(4,8);
          Serial.println(valLeft);
          int power = valLeft.toInt();
          thrusterFront.writeMicroseconds(power);
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
