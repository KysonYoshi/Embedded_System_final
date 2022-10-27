 #include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
#include <Wire.h>

#define RST_PIN         8          
#define SS_PIN          10  //就是模組上的SDA接腳
#define led_pin         9

int I2C_Address = 0xA7 >> 1; // ADXL345 的 I2C 地址
int X0, X1, Y0, Y1, Z1, Z0;
float X,Y,Z;

const int trigPin = 3; //set pin variables
const int echoPin = 2;

const int xInput= A1;
const int yInput= A2;
const int zInput= A3;
int RawMin=0;
int RawMax=1023;
const int sampleSize = 10;

int trigState = LOW; //state of trigPin
int interval = 1; // interval in milliseconds at which trigPin turns on
int interval2 = 1000; //time in milliseconds at which the distance is printed in serial monitors
int printState = LOW; //whether or not to print distance
unsigned long previousMillis = 0; //microsecond at which the pin was last writen
int ledstate=-1;

MFRC522 mfrc522;   // 建立MFRC522實體
Servo myservo1;  // create servo object to control a servo
Servo myservo2;

void setup() {
  pinMode(led_pin,OUTPUT);
  pinMode(trigPin,OUTPUT); //set pinmodes
  pinMode(echoPin,INPUT);
  Serial.begin(9600);
  Serial.print("begin~~~~~~~~~~~~~~~~~~~~\n");
  Wire.begin();  //初始化 I2C
  setReg(0x2D, 0xA); // (打開電源, 設定輸出資料速度為 100 Hz)   
  SPI.begin();        // 初始化SPI介面
  mfrc522.PCD_Init(SS_PIN, RST_PIN); // 初始化MFRC522卡
  Serial.print(F("Reader "));
  Serial.print(F(": "));
  mfrc522.PCD_DumpVersionToSerial(); // 顯示讀卡設備的版本
  myservo1.attach(5);
  myservo2.attach(6);
  myservo1.write(20);                  // sets the servo position according to the scaled value
  myservo2.write(20);
  delay(5000);    
  myservo1.write(90);                  // sets the servo position according to the scaled value
  myservo2.write(90);
}


void loop() {
  rfid();
  Serial.println("ff");
  ultraSonic();
  if (Serial.available() >0){
    Serial.print("plz");
    String data = Serial.readStringUntil('\n');
    if (data=="open"){
      myservo1.write(0);                  // sets the servo position according to the scaled value
      myservo2.write(0);
    }
    else if (data=="close"){
      myservo1.write(90);                  // sets the servo position according to the scaled value
      myservo2.write(90);
    }
    if (data=="light"){
      ledstate*=-1;
    }
    if (ledstate==1){
      digitalWrite(led_pin, HIGH);
      delay(5);
    }else if (ledstate==-1){
      digitalWrite(led_pin, LOW);
      delay(5);
    }
  }
}

void rfid(){
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
      // 顯示卡片內容
      Serial.print(F("Card UID:"));
      dump_byte_array(mfrc522.uid.uidByte, mfrc522.uid.size); // 顯示卡片的UID
      Serial.println();
      Serial.print(F("PICC type: "));
      MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
      Serial.println(mfrc522.PICC_GetTypeName(piccType));  //顯示卡片的類型
      mfrc522.PICC_HaltA();  // 卡片進入停止模式
  }
}

void ultraSonic(){
  unsigned long currentMillis = millis(); //time in milliseconds from which the code was started
  if (currentMillis-previousMillis >= interval) { //check "blink without delay" code
    previousMillis = currentMillis;
    if (trigState == LOW){
      (trigState = HIGH);
    }
    else {
      (trigState = LOW);
    }
  }
  // printing if statement
  if (currentMillis-previousMillis >= interval2) { //check "blink without delay" code
    previousMillis = currentMillis;
    if (printState == LOW){
      (printState = HIGH);
    }
    else {
      (printState = LOW);
    }
  }
  digitalWrite(trigPin,trigState);
  int duration, distance; //variables
  duration = pulseIn(echoPin,HIGH);
  distance = (duration/2) / 29.1;
  if (printState = HIGH && distance!=0){
    Serial.print("distance: ");
    Serial.print(distance);
    Serial.println(" cm");

    int xRaw = ReadAxis(xInput);
    int yRaw = ReadAxis(yInput);
    int zRaw = ReadAxis(zInput);

    long xScaled = map(xRaw, RawMin, RawMax, -3000,3000);
    long yScaled = map(yRaw, RawMin, RawMax, -3000,3000);
    long zScaled = map(zRaw, RawMin, RawMax, -3000,3000);

    float xAccel = xScaled/100.0+7;
    float yAccel = yScaled/100.0+6;
    float zAccel = zScaled/100.0+10;

    Serial.print("X, Y, Z: ");
    Serial.print(xRaw);
    Serial.print(" ");
    Serial.print(yRaw);
    Serial.print(" ");
    Serial.print(zRaw);
    Serial.print(" ");
    Serial.print(xAccel,0);
    Serial.print(" ");
    Serial.print(yAccel,0);
    Serial.print(" ");
    Serial.println(zAccel,0);

    X0 = getData(0x32); // 取得 X 軸 低位元資料
    X1 = getData(0x33); // 取得 X 軸 高位元資料
    X = ((X1 << 8)  + X0) / 256.0;
 
    Y0 = getData(0x34); // 取得 Y 軸 低位元資料
    Y1 = getData(0x35); // 取得 Y 軸 高位元資料
    Y = ((Y1 << 8)  + Y0) / 256.0;
 
    Z0 = getData(0x36); // 取得 Z 軸 低位元資料
    Z1 = getData(0x37); // 取得 Y 軸 高位元資料
    Z = ((Z1 << 8)  + Z0) / 256.0;
    Serial.print("OPEN XYZ: ");
    Serial.print(X);
    Serial.print(" ");
    Serial.print(Y);
    Serial.print(" ");
    Serial.println(Z);

    int VR_position = analogRead(A0);
    int ServoPosition = map(VR_position, 0, 1023, 1, 180);
    Serial.print("photoResister: ");
    Serial.println(ServoPosition);
  }
}

void dump_byte_array(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}

int ReadAxis(int axisPin)
{
long reading=0;
analogRead(axisPin);
delay(1);
for(int i=0; i< sampleSize;i++)
  {
  reading += analogRead(axisPin);
  }
return reading/sampleSize;
}

void setReg(int reg, int data){
    Wire.beginTransmission(I2C_Address);
    Wire.write(reg); // 指定佔存器
    Wire.write(data); // 寫入資料
    Wire.endTransmission();
}

/* getData(reg)：取得佔存器裡的資料
 * 參數：reg → 佔存器位址
 */
int getData(int reg){
    Wire.beginTransmission(I2C_Address);
    Wire.write(reg);
    Wire.endTransmission();
    
    Wire.requestFrom(I2C_Address,1);
    
    if(Wire.available()<=1){
        return Wire.read();
    }
}
