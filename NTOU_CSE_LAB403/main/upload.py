import mysql.connector
import pandas as pd
import cv2
import numpy as np
import io
from io import BytesIO
from PIL import Image
import datetime
import json

with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)
camera_config = config_data['camera_config']
db_config = config_data['GCP_VM_DB']

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
    with open(image_path, 'rb') as f:
        img_data = f.read()

    # 將系統時間格式轉換成 MySQL 的 timestamp 格式
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    sql = "UPDATE frames SET name = %s, data = %s, update_time = %s WHERE id = %s"
    val = (name, img_data, current_time, id)
    mycursor.execute(sql, val)
    fishDB.commit()


if __name__ == '__main__':
  #選擇攝影機
  #參考 https://www.ispyconnect.com/camera/d-link
  cap = cv2.VideoCapture(camera_config['dynacolor02'])

  i = 0
  while(True):
    # 從攝影機擷取一張影像
    ret1, frame1 = cap.read()
    #resize to 720*480
    if ret1:
      frame1 = cv2.resize(frame1,(720,480))
    else:
      break

    if i == 0:
      print(frame1.shape)
      i = 1
    
    # 顯示圖片(720, 480, 3)
    cv2.imshow('monitor', frame1)

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

  # 查詢資料
  result = select_data(id)
  if result[2] is not None:
      print(result[0], result[1])
      image_download = Image.open(io.BytesIO(result[2]))
      image_download.show()

  # 關閉資料庫連線
  fishDB.close()
  # 釋放攝影機
  cap.release()
  # 關閉所有 OpenCV 視窗
  cv2.destroyAllWindows()