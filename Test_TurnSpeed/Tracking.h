//Defining Tracking File
#ifndef TRACKING
#define TRACKING

//Pin and value initialization
#include "PinNum.h"
int RL3=225;
int RL2=32;
int MID=0;
int sensor_reading[5];


void MotorWriting(double vL, double vR) {
  if (vR >= 0) {
    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, HIGH);
  //這邊的Motor第幾個對應到的High/Low是助教的車對應到的，請自己測試自己車該怎麼填！
  } else if (vR < 0) {
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, LOW);
    vR = -vR; //因為analogWrite只吃正數，所以如果本來是負數，就要乘-1
  }
  if (vL >= 0) {
    digitalWrite(BIN2, LOW);
    digitalWrite(BIN1, HIGH);
    //這邊的Motor第幾個對應到的High/Low是助教的車對應到的，請自己測試自己車該怎麼填！
  } else if (vL < 0) {
    digitalWrite(BIN2, HIGH);
    digitalWrite(BIN1, LOW);
    vL = -vL; //因為analogWrite只吃正數，所以如果本來是負數，就要乘-1
  }
  analogWrite(PWMA, vR);
  analogWrite(PWMB, vL);
}

void SensorValue()
{
  for (int i=0; i<5; i++)
  {
   sensor_reading[i] = digitalRead(Sensor_Pin_Value[i]); 
   //Serial.print(sensor_reading[i]);
  }
  //Serial.println();
}

int get_sum()
{
  SensorValue();
  int Sensor_sum=0;
  for (int i=0; i<5; i++)
  {
   Sensor_sum += sensor_reading[i];
  }

  return Sensor_sum;
}

void PControl()
{
  SensorValue();
  int error= -RL3*sensor_reading[0]+
            -RL2*sensor_reading[1]+
            MID*sensor_reading[2]+
            RL2*sensor_reading[3]+
            RL3*sensor_reading[4];
  int SumError=0;
  
  if(get_sum() == 0)
  {
    error = 0 ;
  }
  else
  {
    error = error/get_sum();
  }
  
  if(error>0)
  {
    MotorWriting(200,200-error);

  }
  else{
    MotorWriting(200+error,200); 
  }
}

bool isNode()
{
  if(get_sum() == 5)
  {
      return true;
  }

  return false; 
}

//black --->1





#endif
