import mysql.connector
import pandas as pd
import cv2
import numpy as np
import io
import os
from io import BytesIO
from PIL import Image
import datetime
import json
from mysql.connector import Error
import sys
import datetime


with open('/home/pi/Desktop/NTOU_CSE_LAB403/main/config.json', 'r') as config_file:
    config_data = json.load(config_file)
camera_config = config_data['camera_config']
db_config = config_data['fishDB']

# 連線MySQL資料庫
fishDB = mysql.connector.connect(
  host=db_config['host'],
  user=db_config['user'],
  password=db_config['password'],
  database=db_config['database']
)

# 創建cursor物件
mycursor = fishDB.cursor()

# 新增資料
def insert_data(id, name, image_path):
    with open(image_path, 'rb') as f:
        img_data = f.read()

    # 將系統時間格式轉換成 MySQL 的 timestamp 格式
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    sql = "INSERT INTO frames (id, name, data, update_time) VALUES (%s, %s, %s, %s)"
    val = (id, name, img_data, current_time)
    mycursor.execute(sql, val)
    fishDB.commit()

# 刪除資料
def delete_data(id):
    sql = "DELETE FROM frames WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    fishDB.commit()

# 查詢資料
def select_data(id):
    sql = "SELECT * FROM frames WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    return result

def update_data(id, name, image_path):
    if os.path.exists(image_path):
      with open(image_path, 'rb') as f:
          img_data = f.read()

    # 將系統時間格式轉換成 MySQL 的 timestamp 格式
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    sql = "UPDATE frames SET name = %s, data = %s, update_time = %s WHERE id = %s"
    val = (name, img_data, current_time, id)
    mycursor.execute(sql, val)
    fishDB.commit()
def select_mode():
    sql = "SELECT mode FROM decision WHERE id = %s"  # 修改为你的表名和条件
    val = (1,)  # 你可能需要传递一个合适的 id 值，这里假设为 1
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    
    sql = "SELECT feed_alive FROM cloud_config where id= %s;"  # 修改为你的表名和条件
    val = (1,)  # 你可能需要传递一个合适的 id 值，这里假设为 1
    mycursor.execute(sql, val)
    resultACC = mycursor.fetchone()
    fishDB.commit()
    



    sql = "SELECT blower_state FROM ESP32 ORDER BY date DESC, time DESC LIMIT 1 ;"  #blower_state
    mycursor.execute(sql)
    result_blower_state = mycursor.fetchone()
    if(result_blower_state[0]=="on"):
       result_blower_state=1
    elif(result_blower_state[0]=="off"):
      result_blower_state=0
    else:
      result_blower_state=None
      print(result_blower_state[0])

    return result[0],resultACC[0],result_blower_state if result and resultACC else None  # 返回 mode 值或 None


if __name__ == '__main__':
  #選擇攝影機
  #參考 https://www.ispyconnect.com/camera/d-link
  
  i = 0
  z=0
  result=select_mode()
  mode = result[0]
  Acc=result[1]
  ESP32_blower=result[2]
  cap_exit=0
  print(mode , Acc,ESP32_blower)
  timer=5
  while(timer):
    timer-=1
    try:
        #sys.stdout.flush()
        # 連線MySQL資料庫
        fishDB = mysql.connector.connect(
          host=db_config['host'],
          user=db_config['user'],
          password=db_config['password'],
          database=db_config['database'],
          connect_timeout=10
        )

        # 創建cursor物件
        mycursor = fishDB.cursor()
    except Exception as e:
        print("conn err in 001",e)
        fishDB.close()
        sys.stdout.flush()
        # 連線MySQL資料庫
        continue
    try:    
        result=select_mode()
        mode = int(result[0]
    )
        Acc=int(result[1]
    )
        ESP32_blower=int(result[2])
        
        z+=1
        if((mode + Acc + ESP32_blower)==0):
            cv2.waitKey(10000)
            fishDB.close()
            print(z,mode , Acc,ESP32_blower,((mode + Acc + ESP32_blower)))
        # 從攝影機擷取一張影像
        else:  
            cap = cv2.VideoCapture(camera_config['local'])
            ret1, frame1 = cap.read()
            #resize to 720*480
            if ret1:
              frame1 = cv2.resize(frame1,(720,480))
            else:
              break

            if i == 0:
              print(frame1.shape)
              i = 1
            
            current_time = datetime.datetime.now()
            # 顯示圖片(720, 480, 3)
            #cv2.imshow('monitor', frame1)
            cap_exit=1
            #print(z)
            # 若按下 q 鍵則離開迴圈
            if cv2.waitKey(10000) & 0xFF == ord('q'):
              break
            else:
              cv2.imwrite("/home/pi/Desktop/NTOU_CSE_LAB403/main/upload_frames/upload.png", frame1)
              id = 1
              image_path = '/home/pi/Desktop/NTOU_CSE_LAB403/main/upload_frames/upload.png'
              # 刪除資料
              #delete_data(id)
              # 新增資料
              #insert_data(id, 'picture01', image_path)
              # 更新資料
              update_data(id, 'picture01', image_path)
              #print("fetch")
              cap.release()
        fishDB.close()
    except Exception as e:
        print("conn err:",e)
        fishDB.close()
        sys.stdout.flush()
        # 連線MySQL資料庫
        continue
  # 查詢資料
  """
  result = select_data(id)
  if result[2] is not None:
      print(result[0], result[1])
      image_download = Image.open(io.BytesIO(result[2]))
      image_download.show()
    
    """
  # 關閉資料庫連線
  fishDB.close()
  # 釋放攝影機
  if cap_exit:
      cap.release()
      # 關閉所有 OpenCV 視窗
      cv2.destroyAllWindows()
