/***************************************************************************/
// File       [RFID.h]
// Author     [Erik Kuo]
// Synopsis   [Code for getting UID from RFID card]
// Functions  [rfid]
// Modify     [2020/03/27 Erik Kuo]
/***************************************************************************/

/*===========================don't change anything in this file===========================*/
#include <SoftwareSerial.h>
SoftwareSerial BT (13, 12);
#include <SPI.h>
#include <MFRC522.h>     // 引用程式庫
/* pin---- SDA:9 SCK:13 MOSI:11 MISO:12 GND:GND RST:define on your own  */
#define RST_PIN 5
#define SS_PIN 53
MFRC522 mfrc522(SS_PIN, RST_PIN);  // 建立MFRC522物件

int index;
char uid[8] = {0};

bool detected(){
  if(mfrc522.PICC_IsNewCardPresent()){
    if(mfrc522.PICC_ReadCardSerial()){
      return true;
      }
    }
    return false;
  }

void rfid(){
  delay(10);
  if( mfrc522.PICC_IsNewCardPresent()) {
    if( mfrc522.PICC_ReadCardSerial()) {
      Serial.println(F("Card Detected:"));
      byte *id = mfrc522.uid.uidByte;
      byte idsize = mfrc522.uid.size;
      for(int i=0;i<idsize;i++){
        Serial.print(id[i],HEX);
        Serial.println();
        int rf1, rf2;
        char RF1, RF2;
        rf1 = int(id[i])/16;
        rf2 = int(id[i])%16;
        switch(rf1){
          case 10: RF1 = 'A'; break;
          case 11: RF1 = 'B'; break;
          case 12: RF1 = 'C'; break;
          case 13: RF1 = 'D'; break;
          case 14: RF1 = 'E'; break;
          case 15: RF1 = 'F'; break;
          default: RF1 = rf1 + '0';        
        }
        switch(rf2){
          case 10: RF2 = 'A'; break;
          case 11: RF2 = 'B'; break;
          case 12: RF2 = 'C'; break;
          case 13: RF2 = 'D'; break;
          case 14: RF2 = 'E'; break;
          case 15: RF2 = 'F'; break;
          default: RF2 = rf2 + '0';        
        }
        //BT.write(RF1);
        //BT.write(RF2);
        //BT.write('\n');
        Serial.println(RF1);
        Serial.println(RF2);
        Serial.println('\n');
        index = i*2;
        uid[index] = RF1;
        uid[index+1] = RF2;
      }
      for(int i=0;i<8;i++){
        BT.write(uid[i]);
        uid[i] = 0;
        }
      Serial.println();
      BT.write('\n');
      mfrc522.PICC_HaltA(); // 讓同一張卡片進入停止模式 (只顯示一次)
      mfrc522.PCD_StopCrypto1(); // 停止 Crypto1
    }
  }
}
