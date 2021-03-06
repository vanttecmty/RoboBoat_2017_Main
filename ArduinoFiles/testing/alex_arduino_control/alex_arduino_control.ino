#include <Servo.h>

//Receiver arduino pins
const int PIN_X8R_4 = 6;
const int PIN_X8R_2 = 9;
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
  if (channel5 < 1300) {
     power_Difference();
  }
  else if ( channel5 > 1600) {
      autonomous_Mode();
  }
  else {
      thrusterRight.writeMicroseconds(1500);
      thrusterLeft.writeMicroseconds(1500);
  }
}

void power_Difference() {
  float Y;
  float R;
  float L;

  if ((channel4 > 1450 & channel4 < 1550) & (channel2 > 1450 & channel2 < 1550)){
    R=1500;
    L=1500;
    thrusterRight.writeMicroseconds(R);
    thrusterLeft.writeMicroseconds(L);
  }
  else if ((channel4 > 1450 & channel4 < 1550) & (channel2 < 1450 || channel2 > 1550)) {
    R=map(channel2, 988, 2012, 1100, 1900);
    L=map(channel2, 988, 2012, 1100, 1900);
    thrusterRight.writeMicroseconds(R);
    thrusterLeft.writeMicroseconds(L);
  }
  else if ((channel4 < 1450 || channel4 > 1550) & (channel2 > 1450 & channel2 < 1550)) {
    R = map(channel4, 975, 2025, 1900, 1100);
    L = map(channel4, 975, 2025, 1100, 1900);
    thrusterRight.writeMicroseconds(R);
    thrusterLeft.writeMicroseconds(L);
  }
  else if ((channel4 < 1450) & (channel2 < 1450 || channel2 > 1550)) {
    Y = (channel2-(channel2-1500)*(1500-channel4)/525);
    R = map(channel2, 975, 2025, 1100, 1900);
    L = map(Y, 975, 2025, 1100, 1900);
    thrusterRight.writeMicroseconds(R);
    thrusterLeft.writeMicroseconds(L);
  }
  else if ((channel4 > 1550) & (channel2 < 1450 || channel2 > 1550)) {
    Y = (channel2-(channel2-1500)*(channel4-1500)/525);
    R = map(Y, 975, 2025, 1100, 1900);
    L = map(channel2, 975, 2025, 1100, 1900);
    thrusterRight.writeMicroseconds(R);
    thrusterLeft.writeMicroseconds(L);
  }
}

void autonomous_Mode() {
  // put your main code here, to run repeatedly:
  //while(!Serial.available()) {}
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
      Serial.println(inputString);
      if(inputString[1] == 'B') {
          String valRight = inputString.substring(3,7);
          String valLeft = inputString.substring(8,12);
          //Serial.println(valLeft);
          int powerL = valLeft.toInt();
          int powerR = valRight.toInt();
          
          thrusterRight.writeMicroseconds(powerR);
          Serial.print(powerR);
          thrusterLeft.writeMicroseconds(powerL);
          Serial.print(powerL);
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
        }
    }  
    //Delete Previous Message
     inputString = "";
}

void loop() {
  read_values();
  select();
}
