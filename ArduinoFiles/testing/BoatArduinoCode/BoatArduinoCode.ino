#include <Servo.h>

//Receiver arduino pins
const int PIN_X8R_4 = 6;
const int PIN_X8R_2 = 3;
const int PIN_X8R_5 = 5;

String inputString;

//Receiver channels
float channel4;
float channel2;
float channel5;

//Thrusters 
Servo thrusterRight;
Servo thrusterLeft;
 
void setup() {
  //Pin modes
  pinMode(PIN_X8R_4, INPUT);
  pinMode(PIN_X8R_2, INPUT);
  pinMode(PIN_X8R_5, INPUT);

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

void read_values () {
  //Read channel frequecies
  channel4 = pulseIn(PIN_X8R_4, HIGH);
  channel2 = pulseIn(PIN_X8R_2, HIGH);
  channel5 = pulseIn(PIN_X8R_5, HIGH);
}

void select() {
  //Use channel 5 to select current mode
  if (channel5 < 1400) {
      power_Difference();
      Serial.print("pd");
  } else if ( channel5 > 1600) {
      autonomous_Mode();
      Serial.print("a");
  }else {
      thrusterRight.writeMicroseconds(1500);
      thrusterLeft.writeMicroseconds(1500);
  }
}

void power_Difference() {
  float Y;
  float R;
  float L;


  if ((channel4 > 1470 & channel4 < 1515) & (channel2 > 1470 & channel2 < 1515)){
    thrusterRight.writeMicroseconds(1500);
    thrusterLeft.writeMicroseconds(1500);
  }
  else if ((channel4 > 1470 & channel4 < 1515) & (channel2 < 1470 || channel2 > 1515)) {
    thrusterRight.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
    thrusterLeft.writeMicroseconds(map(channel2, 988, 2012, 1100, 1900));
  }
  else if ((channel4 < 1470 || channel4 > 1515) & (channel2 > 1470 & channel2 < 1515)) {
    R = map(channel4, 975, 2025, 1900, 1100);
    L = map(channel4, 975, 2025, 1100, 1900);
    thrusterRight.writeMicroseconds(R);
    thrusterLeft.writeMicroseconds(R);
  }
  else if ((channel4 < 1470) & (channel2 < 1470 || channel2 > 1515)) {
    Y = (channel2-(channel2-1500)*(1500-channel4)/525);
    R = map(channel2, 975, 2025, 1100, 1900);
    L = map(Y, 975, 2025, 1100, 1900);
    thrusterRight.writeMicroseconds(R);
    thrusterLeft.writeMicroseconds(R);
  }
  else if ((channel4 > 1515) & (channel2 < 1470 || channel2 > 1515)) {
    Y = (channel2-(channel2-1500)*(channel4-1500)/525);
    R = map(Y, 975, 2025, 1100, 1900);
    L = map(channel2, 975, 2025, 1100, 1900);
    thrusterRight.writeMicroseconds(R);
    thrusterLeft.writeMicroseconds(R);
  }
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

    if(inputString.length() > 0 && inputString[inputString.length() - 1] == '%'){
      //Serial.println(inputString);
      if(inputString[0] == 'B') {
          String valLeft = inputString.substring(1,5);
          //Serial.println(valLeft);
          int power = valLeft.toInt();
          thrusterRight.writeMicroseconds(power);
          thrusterLeft.writeMicroseconds(power);
        }
        //Left thrusters
        else if(inputString[0] == 'L') {
          String valLeft = inputString.substring(1,5);
          //Serial.println(valLeft);
          int power = valLeft.toInt();
          thrusterLeft.writeMicroseconds(power);
        }
        //Right thrusters
        else if(inputString[0] == 'R') {
          String valRight = inputString.substring(1,5);
          //Serial.println(valLeft);
          int power = valLeft.toInt();
          thrusterRight.writeMicroseconds(power);
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