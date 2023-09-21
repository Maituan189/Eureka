#include <Arduino.h>
#include <ESP32CAN.h>
#include <CAN_config.h>

CAN_device_t CAN_cfg;               // CAN Config
unsigned long previousMillis = 0;   // will store last time a CAN Message was send
const int interval = 1000;          // interval at which send CAN Messages (milliseconds)
const int rx_queue_size = 10;
String code = "";
String id_str = "";
String s = "", a;
String compare = "1078";
// Receive Queue size
void setup() {
  Serial.begin(115200);
  CAN_cfg.speed = CAN_SPEED_500KBPS;
  CAN_cfg.tx_pin_id = GPIO_NUM_5;
  CAN_cfg.rx_pin_id = GPIO_NUM_4;
  CAN_cfg.rx_queue = xQueueCreate(rx_queue_size, sizeof(CAN_frame_t));
  // Init CAN Module
  ESP32Can.CANInit();
  Serial1.begin(9600, SERIAL_8N1, 21, 22);
  Serial1.write("1");
}
void loop() {
  ////////////////
  if (Serial1.available() >0)
  {
    char a = Serial1.read();
    s = a;
    Serial.println(s);
    Serial.println("");
    s = "";
    if (code == "64")
    {
      Serial1.write("1");
      Serial.print("c1");
    }
    else if (code != "64")
    {
      Serial1.write("2");
      Serial.print("c2");
    }
    else
      Serial1.write(".");
    delay(100);
    Serial1.flush();
  }
  ////////////////
  CAN_frame_t rx_frame;
  if (xQueueReceive(CAN_cfg.rx_queue, &rx_frame, 3 * portTICK_PERIOD_MS) == pdTRUE) {
    if (rx_frame.FIR.B.FF == CAN_frame_std) {
    }
    else {
    }
    if (rx_frame.FIR.B.RTR == CAN_RTR) {
      Serial.printf("%08X", rx_frame.MsgID);
      Serial.printf("\n");
      Serial.printf("%d\r\n", rx_frame.FIR.B.DLC);
    }
    else {
      //      Serial.printf("%08X", rx_frame.MsgID);
      id_str = String(rx_frame.MsgID);
      Serial.print(id_str);
      Serial.printf("\n");
      Serial.printf("%d\r\n", rx_frame.FIR.B.DLC);
      for (int i = 0; i < rx_frame.FIR.B.DLC; i++) {
        //        Serial.printf("%02X ", rx_frame.data.u8[i]);
        if (id_str == "1568" && i == 5)
          code = String(rx_frame.data.u8[i]);
      }
      Serial.print("=");
      Serial.print(code);
      Serial.print("=");
      Serial.printf(".\n");
    }
  }
}
