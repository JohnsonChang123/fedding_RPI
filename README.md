# fedding_RPI

## 目錄
- [養殖現場樹梅派的程式碼與設定檔](#養殖現場樹梅派的程式碼與設定檔)
- [教學資源](#教學資源)
- [crontab](#crontab)
- [部署在養殖現場的 Raspberry Pi](#部署在養殖現場的-raspberry-pi)
  - [main](#main)
  - [video](#video)
  - [download_frames](#download_frames)
  - [RPi2Arduino](#rpi2arduino)
- [更新github最新的repository](#更新github最新的repository)
- [目錄結構](#目錄結構)

## 養殖現場樹梅派的程式碼與設定檔
包含自動上傳、水花影像串流、資料庫紀錄、電流感測器。

## 教學資源
- **RPI 安裝教學**  
  [Raspberry Pi 安裝教學](https://consumesky.notion.site/Raspberry-Pi-67234e0ea87345b4aa4d07739c3fbea9)
- **監視器 & NVR 設定教學**  
  [監視器 & NVR 設定教學](https://www.notion.so/NVR-cef7674b61c445eb944c6f175a19c66f)

## crontab

```bash
0 6 * * * sh /home/pi/Desktop/NTOU_CSE_LAB403/fetch2GCP.sh
@reboot sleep 30 ; sudo sh /home/pi/Desktop/ssh_tunel_GCP.sh
* * * * * sudo -u pi nohup python -u /home/pi/Desktop/NTOU_CSE_LAB403/main/uploadv2.py >> /home/pi/Desktop/NTOU_CSE_LAB403/main/log/uploadframe.log 2>&1 &
```
## 部署在養殖現場的 Raspberry Pi
- ### main
- * user.py 可以用 tkinter 介面執行各功能
- * monitor.py 用 RTSP 查看串流的監視器畫面，現在改用 tkinter 秀出來，並包含一個結束按鈕
- * upload.py 上傳 frame 到 GCP VM DB
- * modify_decision.py 重設 GCP VM DB 中的 decision table
- ### video
- 用來採樣監視器畫面

- 自動區分日期資料夾:

- * recording.py 儲存影像 (每隔 10 分鐘錄製兩段 10 秒鐘的影片)
- * recording_perSecond.py 儲存影像 (每秒儲存一個 frame)
- 不會自動區分日期資料夾:

- * save_mp4.py 儲存影像 (馬上儲存 10 秒鐘的影像)
- * ticktack.py 每隔 10 分鐘執行一次 save_mp4.py
- ### download_frames
- 測試看看是否成功上傳投餌時的影像，並將 GCP VM DB 上的 frame 下載下來。


- ### RPi2Arduino
- 用來和投餌機的 ESP32 進行序列埠通訊
- 電機系使用參數: Baud rate = 115200
- * fetch_to_arduino.py 從 GCP VM DB 拿投餌指令並傳遞給 ESP32

- ## 更新github最新的repository
- 在 cmd 下指令
```bash
git fetch
git reset  --hard origin/main
```
## 目錄結構

```plaintext
NTOU_CSE_Lab403/
├── main/
│   ├── download_frames/
│   │   └── download_frame.py        # 下載串流影像(確認成功用)
│   ├── log/
│   │   ├── savepersec.log           # 儲存nohub savepersec log
│   │   └── uploadframe.log          # 儲存nohub uploadframe log
│   ├── upload_frame/
│   ├── video/
│   │   ├── recording_perSecond.py   # 獲取訓練資料
│   │   ├── -save_mp4.py-            # 棄用
│   │   ├── -recording.py-           # 棄用
│   │   └── -ticktack.py-            # 棄用
│   ├── config.json                   # 攝影機、GCP IP
│   ├── modify_decision.py            # 測試資料庫
│   ├── user.py                       # 測試ALL
│   ├── monitor.py                    # 測試攝影機
│   ├── upload.py                     # 棄用
│   └── uploadv2.py                   # 串流影像
├── RPi2Arduino/
│   ├── communication2.ino
│   ├── fetch_to_arduino.py
│   └── install_library.sh
├── fetch2GCP.sh                       # 上傳訓練資料至GCP
├── rebootsetting.sh                   # 當RPI重開時重啟所有程式
└──watchdogcrentsensor                 # 電流感測器
```

