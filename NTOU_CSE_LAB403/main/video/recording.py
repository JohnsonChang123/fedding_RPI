import pandas as pd
import cv2
import numpy as np
from PIL import Image
from multiprocessing import Process, Queue
from datetime import datetime
import schedule
import time
import os

def image_save(taskqueue, width, height, fps, frames_per_file):

    # 指定影片編碼
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #fourcc = cv2.VideoWriter_fourcc(*'H264')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    writer = None

    while True:
        # 從工作佇列取得影像
        image, frame_counter = taskqueue.get()

        # 若沒有影像則終止迴圈
        if image is None: break

        if frame_counter % frames_per_file == 0:

            if writer: writer.release()

            # 建立 VideoWriter 物件（以時間命名）
            now = datetime.now()
            date_folder = now.strftime("%Y%m%d")  # 以年月日格式建立資料夾名稱
            if not os.path.exists(date_folder):
                os.makedirs(date_folder)

            timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
            video_path = os.path.join(date_folder, f'output-{timestamp}.mp4')

            writer = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

        # 儲存影像
        writer.write(image)

    # 釋放資源
    writer.release()

def rtsp_streaming():
    try:
        # 開啟 RTSP 串流
        cap1 = cv2.VideoCapture('rtsp://Admin:1234@192.168.7.21/cam0/h264')

        # 取得影像的尺寸大小
        width = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 取得影格率
        fps = cap1.get(cv2.CAP_PROP_FPS)

        # 建立工作佇列
        taskqueue = Queue()

        # 計數器
        frame_counter = 0

        # 總錄製幀數（20 秒鐘）
        total_frames = fps * 20

        # 每個檔案的幀數（10 秒鐘）
        frames_per_file = fps * 10

        # 建立並執行工作行程
        proc = Process(target=image_save, args=(taskqueue, width, height, fps, frames_per_file))
        proc.start()

        while frame_counter < total_frames:
            # 從 RTSP 串流讀取一張影像
            ret, frame = cap1.read()

            if ret:
                # 將影像放入工作佇列
                taskqueue.put((frame, frame_counter))
                frame_counter += 1
            else:
                # 若沒有影像跳出迴圈
                break

        # 傳入 None 終止工作行程
        taskqueue.put((None, None))

        # 等待工作行程結束
        proc.join()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # 釋放資源
        cap1.release()
        
if __name__ == '__main__':
    schedule.every(10).minutes.do(rtsp_streaming)

    while True:
        schedule.run_pending()
        time.sleep(1)