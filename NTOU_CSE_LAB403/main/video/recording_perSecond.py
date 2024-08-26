import cv2
import os
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# Resolution
frame_width = 720
frame_height = 480

def save_image(frame):
    # 取得今天日期
    current_date = datetime.now().strftime("frames-%Y%m%d")

    # 檢查今天日期的資料夾是否存在，若不存在就新建一個
    current_dir = os.path.join("", current_date)
    os.makedirs(current_dir, exist_ok=True)

    # 以今天日期為檔名儲存當前frame
    frame_filename = os.path.join(current_dir, f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png")
    cv2.imwrite(frame_filename, frame, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    print(f"👍 影像已儲存: -> {frame_filename}")

def rtsp_connect():
    try:
        # 建立RTSP串流
        cap = cv2.VideoCapture('rtsp://Admin:1234@192.168.7.21/cam0/h264')
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)

        # 檢查是否成功連接
        if not cap.isOpened():
            raise Exception("Cannot connect to Camera ~ ")
        
        # 從攝影機擷取一張影像
        ret, frame = cap.read()
        if not ret:
            raise Exception("Cannot read frames😢")
        frame = cv2.resize(frame, (frame_width, frame_height))
        
        # 顯示影像
        # cv2.imshow('monitor', frame)

        return frame
    except Exception as e:
        print(f"發生錯誤：{e}")
    finally:
        # 釋放資源
        cap.release()
        cv2.destroyAllWindows()

def record():
    # 建立 RTSP 連線
    frame = rtsp_connect()
    # 儲存影像
    save_image(frame)

if __name__ == "__main__":
    # 創建一個 BlockingScheduler 物件
    scheduler = BlockingScheduler()

    # 定義一個工作，在每天的 3:00 到 19:59 之間，每隔 10 秒執行一次 record 函數
    scheduler.add_job(record, 'cron', hour='3-20', second='*/10')

    # 開始排程
    try:
        print('Start Recording-----------')
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        # 如果收到 KeyboardInterrupt 或 SystemExit 信號，停止排程
        scheduler.shutdown()
        print('Interrupt-----------')
    
    """ cron table
    python版本
    sudo crontable -e
    */10 4-19 * * * /usr/bin/python3 /home/pi/Desktop/NTOU_CSE_LAB403/main/video/recording_perSecond.py
    shell版本
    每天凌晨3點執行一次
    0 3 * * * /home/pi/Desktop/NTOU_CSE_LAB403/main/video/record.sh >> /home/pi/logfile.log 2>&1
    """
    """
    # 每天的凌晨4點到晚上7點間，每隔10秒鐘儲存當下的一個frame
    schedule.every().day.at("04:00").to("19:00").every(10).seconds.do(record)
    while True:
        schedule.run_pending()
    """

''' 備用連結
# 格式參考 https://www.ispyconnect.com/camera/d-link
D-Link:
cap = cv2.VideoCapture('rtsp://admin:451466@192.168.1.51/live/profile.0') # 印表機
cap = cv2.VideoCapture('rtsp://admin:227182@192.168.1.21/live/profile.0') # 冷氣
Dynacolor:
cap = cv2.VideoCapture('rtsp://Admin:1234@192.168.7.21/cam0/h264')
cap = cv2.VideoCapture('rtsp://Admin:1234@192.168.50.250/cam0/h264')
cap = cv2.VideoCapture('rtsp://Admin:1234@192.168.50.251/cam0/h264')
'''