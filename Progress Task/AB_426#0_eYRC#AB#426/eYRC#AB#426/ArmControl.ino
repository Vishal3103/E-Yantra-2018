/*
* Team Id : 426
* Author List : Rohan Katkan, Joshua D'Cunha, Vishal Sinha, Nayan Nair
* Filename: ArmControl
* Theme: Ant Bot
* Functions: setup(),loop(),servo.write,servo.attach()
* Global Variables: servo1,servo2
*/
#include <Servo.h>

Servo servo1; //standard servo to lift the arm up
Servo servo2; //mini servo to open or close the arm

void setup() {
  // put your setup code here, to run once:
  //preliminary process to control the servos
  servo1.attach(8);
  servo1.write(180); //initially arm is raised

  servo2.attach(7);
  servo2.write(90); //initially arm is opened
  delay(2000);
}

void loop() {
  // put your main code here, to run repeatedly:
  servo1.write(180); //standard servo brings up arm
  delay(1000);
  servo1.write(120);  //standard servo brings down arm
  delay(1000);
  servo2.write(30);  //mini servo closes arm
  delay(1000);
  servo1.write(180); //standard servo lifts up arm
  delay(2000);
  servo1.write(120); //standard servo brings down arm
  delay(1000);
  servo2.write(90); //mini servo opens arm
  delay(3000);
}
