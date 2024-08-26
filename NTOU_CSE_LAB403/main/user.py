import tkinter as tk
import subprocess

root = tk.Tk()

def run_monitor():
    subprocess.Popen(["python", "/home/pi/Desktop/NTOU_CSE_LAB403/main/monitor.py"])
def run_inone():
    subprocess.Popen(["python", "/home/pi/Desktop/NTOU_CSE_LAB403/main/upload.py"])
def run_toESP32():
    subprocess.Popen(["python", "/home/pi/Desktop/NTOU_CSE_LAB403/RPi2Arduino/fetch_to_arduino.py"])
def run_reset_command():
    subprocess.Popen(["python", "/home/pi/Desktop/NTOU_CSE_LAB403/main/modify_decision.py"])
def run_recording():
    subprocess.Popen(["python", "/home/pi/Desktop/NTOU_CSE_LAB403/main/video/recording.py"])
def run_recording_perSecond():
    subprocess.Popen(["python", "/home/pi/Desktop/NTOU_CSE_LAB403/main/video/recording_perSecond.py"])  
def stop_program():
    root.destroy()


button1 = tk.Button(root, text="查看本地監視器", command=run_monitor)
button2 = tk.Button(root, text="上傳監視器影像", command=run_inone)
button3 = tk.Button(root, text="傳遞指令給ESP32", command=run_toESP32)
button4 = tk.Button(root, text="重設GCP VM DB的投餌指令", command=run_reset_command)
button5 = tk.Button(root, text="開始錄製v1", command=run_recording)
button6 = tk.Button(root, text="開始錄製v2", command=run_recording_perSecond)
button7 = tk.Button(root, text="關閉", command=stop_program)


button1.pack()
button2.pack()
button3.pack()
button4.pack()
button5.pack()
button6.pack()
button7.pack()

root.mainloop()
