//Receiver arduino pins
const int PIN_X8R_4 = 6;
const int PIN_X8R_2 = 9;
const int PIN_X8R_5 = 5;

float channel4;
float channel2;
float channel5;

void setup(){
  pinMode(PIN_X8R_4,INPUT);
  pinMode(PIN_X8R_2,INPUT);
  pinMode(PIN_X8R_5,INPUT);  
  Serial.begin(115200);
}

void loop(){
  channel4 = pulseIn(PIN_X8R_4, HIGH);
  channel2 = pulseIn(PIN_X8R_2, HIGH);
  channel5 = pulseIn(PIN_X8R_5, HIGH);
  //channel4 = map(pulseIn(PIN_X8R_4, HIGH), 1150, 2650, 900,2025);
  Serial.print("Palanca Izquierda ");
  Serial.println(channel4);
  //channel2 = map(pulseIn(PIN_X8R_2, HIGH), 1150, 2650, 900,2025);
  Serial.print("Palanca Derecha ");
  Serial.println(channel2);
  //channel5 = map(pulseIn(PIN_X8R_5, HIGH), 1150, 2650, 900,2025);
  Serial.print("Palanca Arriba ");
  Serial.println(channel5);
}


