// Arduino Nano
#include <VirtualWire.h>            // Declara la librería para comunicación.
//#include <Servo.h>                  // Declara la librería para servomotores.
 
const int dataPin = 2;              // Declara la variable dataPin como entero de lectura en el pin 12.
const int ledPin = 13;              // Declara la variable ledPin como entero de lectura en el pin 13.
const int dataPinR = 3;             // Declara la variable dataPinR como entero de lectura en el pin 3.
//Servo servo1;                       // Declara la variable servo1 como Servo.
//Servo servo2;                       // Declara la variable servo2 como Servo.
 
void setup()
{
    //servo1.attach(9);               // Define a la varible servo 1 el pin 9 del arduino.
    //servo2.attach(10);              // Define a la varible servo 2 el pin 10 del arduino.
    Serial.begin(9600);             // Comienza la comunicación con el arduino a 9600 bits/s.
    vw_setup(2000);                 // Configura la velocidad de transmisión de datos a 2000.
    vw_set_tx_pin(dataPin);         // Configura el pin 2 (dataPin) como transmisor de datos.
    vw_set_rx_pin(dataPinR);        // Configura el pin 3 (dataPinR) como recepetor de datos.
    vw_rx_start();                  // Comienza a recibir datos.
}
 
void loop()
{
    uint8_t buf[VW_MAX_MESSAGE_LEN];      //
    uint8_t buflen = VW_MAX_MESSAGE_LEN;  //

    if (vw_get_message(buf, &buflen)) 
    {
      digitalWrite(ledPin, true);
      Serial.print("Mensaje: ");
      for (int i = 0; i < buflen; i++)
      {
         Serial.print((char)buf[i]);
      }
        String val = (char*)buf;                // Convierte el buffer a String.
        String sDir = val.substring(2,3);
        String sNum1 = val.substring(4,7);      
        String sNum2 = val.substring(8,11);
        Serial.println("");
        Serial.print(val[0]);     
        Serial.println("");
        Serial.print(sDir);
        int Num1 = sNum1.toInt();
        //servo1.write(Num1);
        Serial.println("");
        Serial.print(Num1);
        int Num2 = sNum2.toInt();
        //servo2.write(Num2);
        Serial.println("");
        Serial.print(Num2);
        Serial.println("");
        digitalWrite(ledPin, false);
    }
    else {

      const char enviado[256];
      String msg;
      msg = Serial.readString();
      msg.toCharArray(enviado, 256);

      digitalWrite(ledPin, true);
      vw_send((uint8_t *)enviado, strlen(enviado));
      vw_wait_tx();
      digitalWrite(ledPin, false);
    }
}
