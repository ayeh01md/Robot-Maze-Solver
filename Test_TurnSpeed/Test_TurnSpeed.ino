//Including Different Header Files and Pins
#include <SoftwareSerial.h>
#include "PinNum.h"
#include "Tracking.h"
#include "RFID.h"
#include <SPI.h>
#define rxPIN 13
#define txPIN 12

#define RST_PIN 5
#define SS_PIN 53


// 腳位設定 (資料型別設定)
//Initialization
char val[100];
int num = 0;

//Setup for Pins and BT
void setup() {
  pinMode(PWMA, OUTPUT);
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);
  pinMode(PWMB, OUTPUT);
  pinMode(STBY, OUTPUT);
  pinMode(rxPIN, INPUT);
  pinMode(txPIN, OUTPUT);

  Serial.begin (9600);
  BT.begin(9600);
  Serial.println("Bluetooth is ready");
  SPI.begin();
  mfrc522.PCD_Init();

}

//Main Loop
void loop() {
  // put your main code here, to run repeatedly:

  //PUT CHAR ARRAY IN HERE
  digitalWrite(STBY, HIGH);
  //Reading information from bluetooth
  
  while (BT.available() ) {
    if (BT.available() > 0) {
      val[num] = BT.read();
      //Serial.println(val[num]);
      num++;
      //delay(100);
    }
  }

  for(int i =1; i<= num; i++){
    while(isNode() == false){
      PControl();
      if(detected){
        rfid();
      }
    }
    MotorWriting(0,0);
    delay(10);
    Serial.println(val[i]);
    //Detects if next command is straight and executes it
    if (val[i] == 's') {
      MotorWriting(255, 225);
      delay(550);
      
    }

    //Detects if next command is turn backwards and executes it
    if (val[i] == 'b') {
      //Serial.println('b');
      MotorWriting(-200, 200);
      delay(685);
      //MotorWriting(0,0);
      //delay(10);

    //Detects if next command is turn right and executes it      
    }
    if (val[i] == 'r') {
      //Serial.println('r');
      MotorWriting(255, 255);
      delay(250);
      MotorWriting(255, 0);
      delay(575);
    }

    //Detects if next command is turn left and executes it    
    if (val[i] == 'l') {
      MotorWriting(255, 255);
      delay(250);
      MotorWriting(25, 255);
      delay(575);
    }
    
    //Detects if next command is stop and executes it    
    if (val[i] == 't') {
      while(isNode() == true){
        MotorWriting(0, 0);
      }
      delay(1000);
    }
  }

}



//Continued on NODE
//RFID CARD IS AT THE END OF THE PATHS, DO NOT SCAN WHOLE MAZE
