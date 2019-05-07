/*
* Team Id : 426
* Author List : Rohan Katkan, Joshua D'Cunha, Vishal Sinha, Nayan Nair
* Filename: Line_Sensor_PID2
* Theme: Ant Bot
* Functions: setup(),loop(),read_sensor_values(),calculate_pid(),motot_control()
* Global Variables: float Kp=17,Ki=0.3,Kd=10;
volatile float error=0, P=0, I=0, D=0, PID_value=0;
volatile float previous_error=0, previous_I=0;
volatile int Sensor[3]= {0, 0, 0};
int initial_motor_speed=150;
int k=0; //k is to count the no of nodes, central node is the second node
*/


#include <Servo.h> 
float Kp=17,Ki=0.3,Kd=10;
volatile float error=0, P=0, I=0, D=0, PID_value=0;
volatile float previous_error=0, previous_I=0;
volatile int Sensor[3]= {0, 0, 0};
int initial_motor_speed=150;
int k=0;
void read_sensor_values(void);
void calculate_pid(void);
void motor_control(void);

void setup()
{
 pinMode(9,OUTPUT); //PWM Pin 1
 pinMode(6,OUTPUT); //PWM Pin 2
 pinMode(2,OUTPUT); //Left Motor Pin 1
 pinMode(3,OUTPUT); //Left Motor Pin 2
 pinMode(4,OUTPUT); //Right Motor Pin 1
 pinMode(5,OUTPUT);  //Right Motor Pin 2
 Serial.begin(9600); //Enable Serial Communications
  digitalWrite(2,1);
   digitalWrite(3,0);
   digitalWrite(4,1);
   digitalWrite(5,0);
   analogWrite(6, 160);
   analogWrite(9, 150);
   delay(2000);
}

void loop()
{
    read_sensor_values();
    calculate_pid();
    motor_control();
}

void read_sensor_values()
{
  Sensor[0]=digitalRead(A0);
  Sensor[1]=digitalRead(A1);
  Sensor[2]=digitalRead(A2);
  Serial.print("value1: "); Serial.println(Sensor[0]);
  Serial.print("value2: "); Serial.println(Sensor[1]);
  Serial.print("value3: "); Serial.println(Sensor[2]);
   if(Sensor[0]==true && Sensor[1]==false && Sensor[2]==false){
    error=-2;
  }
  //setting value to 1 1 0
  else if(Sensor[0]==true && Sensor[1]==true && Sensor[2]==false){
    error=-1;
  }
  //setting value to 0 1 0 
  else if(Sensor[0]==false && Sensor[1]==true && Sensor[2]==false){
    error=0;
  }
  //setting value to 0 1 1 
  else if(Sensor[0]==false && Sensor[1]==true && Sensor[2]==true){
    error=1;
  }
  //setting value to 0 0 1 
  else if(Sensor[0]==false && Sensor[1]==false && Sensor[2]==true){
    error=2;
  }
  else if((Sensor[0]==0)&&(Sensor[1]==0)&&(Sensor[2]==0))
    if(error==-2) error=-3;
    else error=3;
  else if((Sensor[0]==1)&&(Sensor[1]==1)&&(Sensor[2]==1))
  {
  if(k==2){ //if it detects the central node
  analogWrite(9,85); // go forward a little bit
  analogWrite(6,85);
  digitalWrite(2,1);
   digitalWrite(3,0);
   digitalWrite(4,1);
   digitalWrite(5,0);
   delay(1000);
    digitalWrite(2,0); //stop for some time
   digitalWrite(3,0);
   digitalWrite(4,0);
   digitalWrite(5,0);
   delay(2000);
   digitalWrite(2,1); //rotate clockwise Read SIM1 around 45 degrees
   digitalWrite(3,0);
   digitalWrite(4,0);
   digitalWrite(5,1);
   delay(600);
   Serial.write('1'); //to send a value 1 to rpi (master) so that it will run the python code to take the image of the arena so that it can capture sim1 aruco marker
     digitalWrite(2,0); //stop
   digitalWrite(3,0);
   digitalWrite(4,0);
   digitalWrite(5,0);
   delay(2000);
   digitalWrite(2,1); //then rotate around 90 degrees to capture sim2
   digitalWrite(3,0);
   digitalWrite(4,0);
   digitalWrite(5,1);
   delay(1300);
    digitalWrite(2,0); //stop
   digitalWrite(3,0);
   digitalWrite(4,0);
   digitalWrite(5,0);
   delay(2000);
   digitalWrite(2,1); //rotate clockwise 90 for sim3
   digitalWrite(3,0);
   digitalWrite(4,0);
   digitalWrite(5,1);
   delay(1500);
   digitalWrite(2,0); //stop
   digitalWrite(3,0);
   digitalWrite(4,0);
   digitalWrite(5,0);
   delay(2000);
   digitalWrite(2,1);//rotate clockwise 90 degrees for sim0
   digitalWrite(3,0);
   digitalWrite(4,0);
   digitalWrite(5,1);
   delay(1500);
   digitalWrite(2,0); //stop
   digitalWrite(3,0);
   digitalWrite(4,0);
   digitalWrite(5,0);
   delay(2000)
   digitalWrite(2,1);//rotate clockwise 45 degrees for coming back to original position
   digitalWrite(3,0);
   digitalWrite(4,0);
   digitalWrite(5,1);
   delay(700);
   digitalWrite(2,0); //stop
   digitalWrite(3,0);
   digitalWrite(4,0);
   digitalWrite(5,0);
   delay(2000)
   exit(0);
  }  
  else{ //keep counting until central node detected
 k++;} 
  }
}

void calculate_pid()
{
    P = error;
    I = I + previous_I;
    D = error-previous_error;
    
    PID_value = (Kp*P) + (Ki*I) + (Kd*D);
    
    previous_I=I;
    previous_error=error;
}

void motor_control()
{
    // Calculating the effective motor speed:
    int left_motor_speed = initial_motor_speed-PID_value;
    int right_motor_speed = initial_motor_speed+PID_value;
    
    // The motor speed should not be more than the max PWM value
    constrain(left_motor_speed,0,255);
    constrain(right_motor_speed,0,255);
    analogWrite(6,left_motor_speed);
  analogWrite(9,right_motor_speed);
    //following lines of code are to make the bot move forward
    digitalWrite(2,1);
    digitalWrite(3,0);
    digitalWrite(4,1);
    digitalWrite(5,0);
}
