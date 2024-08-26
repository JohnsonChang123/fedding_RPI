import serial
import mysql.connector
from datetime import datetime
import time
import os
import json

with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)
db_config = config_data['GCP_VM_DB']

# 連線MySQL資料庫
fishDB = mysql.connector.connect(
  host=db_config['host'],
  user=db_config['user'],
  password=db_config['password'],
  database=db_config['database']
)

# 建立和Arduino的實體序列埠通訊
#ser = serial.Serial('COM3', 9600) # Windows 用COMX
#ser = serial.Serial('/dev/ttyACM0', 9600) # Linux 用/dev/ttyACMX
ser = serial.Serial('/dev/ttyUSB0', 115200)
#############################################################
# 每隔 fetch_interval 查詢一次指令(包含fetch_interval，可以在GCP的table : decision更改查詢指令的間隔)
fetch_interval = 10

while True:
    ###### 與 GCP VM DB 連線並取得投餌指令
    try:
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            cursor = connection.cursor()

            # 查詢
            select_query = "SELECT * FROM decision WHERE id = 1"

            cursor.execute(select_query)
            result = cursor.fetchone()

            if result:
                id, mode, angle, period, amount, fetch_interval = result
                print(f"投餌指令: mode: {mode}, angle: {angle}, period: {period}, amount: {amount}, fetch_interval: {fetch_interval}")
                #id = result
                #print(id)
                new_fetch_interval = fetch_interval
            else:
                print("找不到指令")

            connection.commit()
            print("指令獲取成功")

    except mysql.connector.Error as err:
        # 若RPi和GCP的連線失敗，則傳遞備用指令給ESP32 (定時模式 3小時)
        id, mode, angle, period, amount, fetch_interval = 1, 2, 90, 180, 10, 5 
        print("Database Connection FAILED-:", err)

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")
    #####-------------------------------------------

    ##### 向Arduino傳遞投餌指令，並確認回傳值是否正確
    try:
        # 傳送訊息到Arduinn
        to_send = f"{mode}{angle}{period}{amount}{fetch_interval}"
        ser.write(to_send.encode())

        # 從Arduino接收資料
        arduino_response = ser.readline().decode().strip()
        print("Arduino回傳收到指令: ", arduino_response)
        """ R
        print(to_send)
        print(arduino_response)
        if arduino_response.strip() == to_send.strip():
            print("Arduino正確接收: ", arduino_response)
        else:
            print("Arduino接收異常: ", arduino_response)
        """
    except serial.SerialException as e:
        print("Arduino端異常: ", e)
    #####-------------------------------------------

    # set time interval
    new_fetch_interval = int(new_fetch_interval)
    time.sleep(new_fetch_interval)
    print("***")
# 關閉串列通訊物件
ser.close()