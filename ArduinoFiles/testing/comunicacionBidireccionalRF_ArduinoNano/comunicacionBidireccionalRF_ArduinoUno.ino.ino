// Arduino Uno
#include <VirtualWire.h>
//#include <Servo.h>
 
const int dataPin = 2;
const int ledPin = 13;
const int dataPinT = 3;
//Servo servo1;
//Servo servo2;

void setup()
{
    
  //servo1.attach(11);
  //servo2.attach(10);
    Serial.begin(9600);
    vw_setup(2000);
    vw_set_tx_pin(dataPinT);
    vw_set_rx_pin(dataPin);
    vw_rx_start();
}
 
void loop()
{
    uint8_t buf[VW_MAX_MESSAGE_LEN];
    uint8_t buflen = VW_MAX_MESSAGE_LEN;
    
    if (vw_get_message(buf, &buflen)) 
    {
      digitalWrite(ledPin, true);
      Serial.print("Mensaje: ");
      for (int i = 0; i < buflen; i++)
      {
         Serial.print((char)buf[i]);
      }
        
        String val = buf;
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
