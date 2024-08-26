# 部署在養殖現場的 Raspberry Pi
有兩個資料夾: main 和 RPi2Arduino

## main
    user.py 可以用 tkinter 介面執行各功能  
    monitor.py 用 RTSP 查看串流的監視器畫面，現在改用 tkinter 秀出來，並包含一個結束按鈕
    upload.py 上傳 frame 到 GCP VM DB  
    modify_decision.py 重設 GCP VM DB 中的 decision table  

### video
    用來採樣監視器畫面

    自動區分日期資料夾:
    recording.py 儲存影像(每隔 10 分鐘錄製兩段 10 秒鐘的影片)
    recording_perSecond.py 儲存影像(每秒儲存一個 frame)

    不會自動區分日期資料夾:
    save_mp4.py 儲存影像(馬上儲存 10 秒鐘的影像)
    ticktack.py 每隔 10 分鐘執行一次 save_mp4.py

### download_frames
    測試看看是否成功上傳投餌時的影像
    把 GCP VM DB 上的 frame 下載下來

## RPi2Arduino
    用來和投餌機的 ESP32 進行序列埠通訊  
    電機系使用參數: Baud rate = 115200  

    fetch_to_arduino.py 從 GCP VM DB 拿投餌指令並傳遞給 ESP32  


## 更新github最新的repository
    在 cmd 下指令
    ```bash
    git fetch
    git reset  --hard origin/main
    ```