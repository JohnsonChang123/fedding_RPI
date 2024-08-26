# fedding_RPI
養殖現場樹梅派的程式碼與設定檔
包含自動上傳、水花影像串流、資料庫紀錄、電流感測器
# RPI 安裝教學
https://consumesky.notion.site/Raspberry-Pi-67234e0ea87345b4aa4d07739c3fbea9
# 監視器 & NVR 設定教學
https://www.notion.so/NVR-cef7674b61c445eb944c6f175a19c66f
# 目錄 
-NTOU_CSE_Lab403
    --main
        ---download_frames
            ----download_frame.py        下載串流影像(確認成功用)
        ---log                           
            ----savepersec.log           儲存nohub savepersec log
            ----uploadframe.log          儲存nohub uploadframe log
        ---upload_frame
        ---video
            ----recording_perSecond.py   獲取訓練資料
            ---- -save_mp4.py-             棄用
            ---- -recording.py-            棄用
            ---- -ticktack.py-              棄用
        ---config.json                   攝影機、GCP IP
        ---modify_decision.py            測試資料庫
        ---user.py                       測試ALL
        ---monitor.py                    測試攝影機
        ---upload.py                     棄用
        ---uploadv2.py                   串流影像
    --RPi2Arduino      
        ---communication2.ino
        ---fetch_to_arduino.py
        ---install_library.sh
    --fetch2GCP.sh                       上傳訓練資料至GCP
    --rebootsetting.sh                   當RPI重開時重啟所有程式
