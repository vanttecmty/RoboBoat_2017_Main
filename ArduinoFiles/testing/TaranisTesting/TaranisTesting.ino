//Receiver arduino pins
const int PIN_X8R_4 = 6;
const int PIN_X8R_2 = 3;
const int PIN_X8R_5 = 9;

float channel4;
float channel2;
float channel5;

void setup(){
  pinMode(PIN_X8R_4,INPUT);
  pinMode(PIN_X8R_2,INPUT);
  pinMode(PIN_X8R_5,INPUT);

  delay(1000);
  Serial.begin(115200);
}

void loop(){
  //channel4 = map(pulseIn(PIN_X8R_4, HIGH), 1150, 2650, 900,2025);
  Serial.print("Palanca Izquierda ");
  Serial.println(pulseIn(PIN_X8R_4, HIGH));
  //channel2 = map(pulseIn(PIN_X8R_2, HIGH), 1150, 2650, 900,2025);
  Serial.print("Palanca Derecha ");
  Serial.println(pulseIn(PIN_X8R_2, HIGH));
  //channel5 = map(pulseIn(PIN_X8R_5, HIGH), 1150, 2650, 900,2025);
  Serial.print("Palanca Arriba ");
  Serial.println(pulseIn(PIN_X8R_5, HIGH));
  delay(2000);
  }


