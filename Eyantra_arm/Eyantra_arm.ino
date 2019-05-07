#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;     
String serial;
int serv, val;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  servo1.attach(3);
  servo2.attach(5);
  servo3.attach(6);
  //servo1.write(0);

  servo4.attach(9);
  /*servo2.write(0);
  servo3.write(0);
  servo4.write(0);*/
  delay(2000);
}

void loop() {
  // put your main code here, to run repeatedly:
  servo1.write(180);
  delay(2000);
  servo1.write(0);
  delay(5
  000);
  /*
  servo1.write(120);
  delay(1000);
  servo2.write(30);
  delay(1000);
  servo1.write(180);
  delay(2000);
  servo1.write(120);
  delay(1000);
  servo2.write(90);
  delay(3000);
  servo1.write(180);60
  delay(5000);
  servo1.write(0);
  delay(5000);*/

 /* if (Serial.available()>0){
    serial = Serial.readStringUntil('\n');
    serv = serial.substring(0,1).toInt();
    val = serial.substring(1).toInt();
    Serial.print(serv);
    Serial.print(val);
  }
  
  switch(serv){
    case 3:
      servo1.write(val);
      break;
    case 5:
      servo2.write(val);
      break;
    case 6:
      servo3.write(val);
      break;
    case 9:
      servo4.write(val);
      break;
   }*/
}
