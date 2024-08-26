import mysql.connector
import pandas as pd
import cv2
import numpy as np
import io
from io import BytesIO
from PIL import Image
import time
import json

with open('/home/pi/Desktop/NTOU_CSE_LAB403/main/config.json') as config_file:
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

    sql = "INSERT INTO frames (id, name, data) VALUES (%s, %s, %s)"
    val = (id, name, img_data)
    mycursor.execute(sql, val)
    fishDB.commit()

# 刪除資料
def delete_data(id):
    sql = "DELETE from frames WHERE id = %s"
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

# main
def download_frames(count):
    id = 1

    image_path = '/home/pi/Desktop/NTOU_CSE_LAB403/main/download_frames/' + str(count) + ".png"
    # image_path = 'C://11157065//lab//yunlin//newGCP//download_frames//ar1//test' + str(count) + ".png"
    duration = 3
    start_time = time.time()

    # 查詢資料
    result = select_data(id)
    if result[2] is not None:
        print(result[0], result[1])
        image_download = Image.open(io.BytesIO(result[2]))
        image_download.save(image_path,"png")
        image_download.show()

    # 刪除資料
    #delete_data(id)

    # 關閉資料庫連線
    fishDB.close()

count = 1
download_frames(count)