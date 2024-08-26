import schedule
import time
import subprocess

def call_another_program():
    # 在這裡執行你想要呼叫的程式
    subprocess.call(['python', 'save_mp4.py'])

# 設定定時任務，每隔一段時間呼叫 call_another_program 函數
schedule.every(10).minutes.do(call_another_program)  # 每分鐘執行一次
# schedule.every().hour.do(call_another_program)  # 每小時執行一次
# schedule.every().day.at("10:30").do(call_another_program)  # 每天的 10:30 執行一次

while True:
    schedule.run_pending()
    time.sleep(1)
