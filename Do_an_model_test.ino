#include <Wire.h>
#include <BH1750.h>
#include <DHT.h>
#include <Preferences.h> //Thư viện hỗ trợ lưu flash

//Define loai cam bien DHT
#define DHTTYPE DHT22

//Thong so mac dinh
int dhtPin = 15;      // Chân mặc định cho DHT
int ledPin = 13;       // LED mặc định
bool ledState = false;  //Tat LED theo mac dinh
int SDA_PIN=20 ;
int SCL_PIN=21;
int sendInterval = 2000; //Khoang thoi gian cho moi khi gui tin hieu (ms)
// bool bh1750_ok = false;


//Tao doi tuong cam bien DHT22
DHT dht(dhtPin, DHTTYPE);

//Tao doi tuong cam bien anh sang
BH1750 lightMeter;//Thu vien - ten cam bien

Preferences prefs; //Doi tuong luu Preferences

// bool isI2CDeviceConnected(uint8_t address) {
//   Wire.beginTransmission(address);
//   return Wire.endTransmission() == 0;
// }


// bool isBH1750Connected() {
//   return isI2CDeviceConnected(0x23) || isI2CDeviceConnected(0x5C);
// }

void setup() {
  //Mở cổng serial với baud rate 115200
  Serial.begin(115200);

  esp_log_level_set("BH1750", ESP_LOG_NONE);


  //Chỉ log một số lỗi nhất định
  esp_log_level_set("i2c", ESP_LOG_WARN); // Hoặc ESP_LOG_ERROR để chỉ in lỗi nghiêm trọng

  //Tắt toàn bộ log từ thư viện/hệ thống
  esp_log_level_set("*", ESP_LOG_NONE);  // Tắt log toàn bộ hệ thống (mọi module)

  // delay(1000);  //Delay chờ code python, sửa lại nếu cần

  // Serial.println("=INIT=");

  // Đọc từ bộ nhớ không mất khi reset
  // prefs.begin("i2c-pins", false); // namespace "i2c-pins", false = read + write
  // SDA_PIN = prefs.getInt("sda", 20); // Nếu chưa có thì dùng mặc định GPIO 21
  // SCL_PIN = prefs.getInt("scl", 21); // Mặc định GPIO 22

  // Kiểm tra xem đã từng lưu chưa
  // if (!prefs.isKey("sda") || !prefs.isKey("scl")) {
  //   // Ghi giá trị mặc định vào flash để không bị "mất"
  //   prefs.putInt("sda", SDA_PIN);
  //   prefs.putInt("scl", SCL_PIN);
  //   // Serial.println("Lần đầu chạy - đã lưu mặc định SDA/SCL vào flash");
  // }

  // prefs.end();

  //Lấy chân DHT22 và LED trước đó
  prefs.begin("pins", false); // namespace là "pins"

  // Lấy giá trị đã lưu, nếu không có thì dùng mặc định
  dhtPin = prefs.getInt("dht", 15);
  ledPin = prefs.getInt("led", 13);


  //Khởi chạy các linh kiện
  //LED
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  ledState = false;

  // DHT
  dht.begin();
  delay(100);

  //BH1750FVI

  Wire.begin(SDA_PIN, SCL_PIN);
  delay(50);  
  lightMeter.begin();
  
  //Kiểm tra kết nối các cảm biến
  
  //DHT22
  if (isnan(dht.readTemperature()) || isnan(dht.readHumidity())) {
    Serial.println("DHTNOTFOUND");
  } else {
    Serial.println("DHT22OK");
  }

  //BH1750FVI

  //Debug doc data tu prefs
  // Serial.print("Dùng SDA: "); Serial.println(SDA_PIN);
  // Serial.print("Dùng SCL: "); Serial.println(SCL_PIN);
  // delay(50);
  // Wire.begin(SDA_PIN, SCL_PIN);
  // delay(50);

  if (lightMeter.begin()) {
    Serial.println("BH1750OK");
    // bh1750_ok = true; 
  } else {
    Serial.println("BH1750NOTFOUND");
  }
  //   Serial.println("Vui long rut nguon va cam lai nguon");
  //   bh1750_ok = false;
  //loop kiểm tra chân vật lý đã cắm chưa
  // bool isConnected = 1;
    
  // }
  // //Loop chờ cắm lại chân
  // while (!bh1750_ok){
  //   if (!isBH1750Connected()){
  //     Serial.println("Đang chờ cắm lại chân");
  //     delay(1000);

  //   }
  //   else{
  //     Serial.println("Đã cắm lại cảm biến BH1750");

  //     if (lightMeter.begin()) {
  //       bh1750_ok = true;
  //       Serial.println("BH1750 khởi động thành công!");
  //     }
      
  //     delay(1000);
  //   }
  // }
  //Kiểm tra module
  Serial.println("ESPOK");
}




void loop() {

  static unsigned long lastSend = 0;
  //Gửi output định kỳ
  if (millis() - lastSend >= sendInterval) {
    
    //DHT22
    float temp = dht.readTemperature();
    float hum = dht.readHumidity();
    float lux = NAN;

    // if (bh1750_ok) {

    // }
  
    lux = lightMeter.readLightLevel();

    // Xử lý giá trị bất thường
    if (lux < 0.0 || lux >= 100000.0) lux = NAN;

    Serial.print("TEMP:");
    Serial.print(temp);
    Serial.print(";HUM:");
    Serial.print(hum);
    Serial.print(";LUX:");
    Serial.print(lux);
    Serial.print(";LED:");
    Serial.println(ledState ? "ON" : "OFF");

    lastSend = millis();
  }

  //Đọc output từ python
  if (Serial.available()) {

    //Xử lý input từ python
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    //DHT22
    if (cmd.startsWith("SET_DHT_PIN:")) {
      //Debug, đừng quan tâm
      // Serial.print("[DEBUG] Received string: ");
      // Serial.println(cmd);  // Kiểm tra chuỗi thực tế nhận được

      // String pinStr = cmd.substring(13);
      // Serial.print("[DEBUG] Extracted pin: ");
      // Serial.println(pinStr);

      int newPin = cmd.substring(12).toInt();
      dht = DHT(newPin, DHTTYPE);
      dht.begin();
      dhtPin = newPin;

      // Lưu vào flash
      prefs.begin("pins", false);
      prefs.putInt("dht", newPin);
      prefs.end();
      
      Serial.print("DHTPINUPDATED");
      Serial.println(newPin);
    } 

    //BH1750FVI
    // else if (cmd.startsWith("SET_BH1750_PINS:")) {
    //   int splitIdx = cmd.indexOf(',');
    //   int newSDA = cmd.substring(16, splitIdx).toInt();
    //   int newSCL = cmd.substring(splitIdx + 1).toInt();


    //   prefs.begin("i2c-pins", false);
    //   prefs.putInt("sda", newSDA);
    //   prefs.putInt("scl", newSCL);
    //   prefs.end();

    //   Serial.println("BH1750PINSUPDATED");

    //   // Wire.begin (newSDA,newSCL);

    //   ESP.restart(); // Reset lại để áp dụng
    // }


    //LED

    //Đổi chân:
    else if (cmd.startsWith("SET_LED_PIN:")) {

      // int splitIdx = cmd.indexOf(',');
      int newLED = cmd.substring(12).toInt();

      pinMode(ledPin, INPUT); // Ngừng dùng chân cũ
      digitalWrite(ledPin, LOW); // Đảm bảo không còn HIGH

      ledPin = newLED;
      pinMode(ledPin, OUTPUT);
      digitalWrite(ledPin, LOW);

      //Lưu lại
      prefs.begin("pins", false);
      prefs.putInt("led", newLED);

      prefs.end();
      Serial.println("LEDPINUPDATED");

      // ledState = false;

    }
    //Bật/ tắt
    else if (cmd == "LED_ON") {
      digitalWrite(ledPin, HIGH);
      ledState = true;
      Serial.println("LEDON");
    } 
    else if (cmd == "LED_OFF") {
      digitalWrite(ledPin, LOW);
      ledState = false;
      Serial.println("LEDOFF");
    }
  }
}