import cv2
import json
import tkinter as tk
from PIL import Image, ImageTk

def on_closing():
    root.destroy()

def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (720, 480))

        # fromarray轉成PIL；PhotoImage轉成tkinter可以顯示的格式
        photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo

        root.after(10, lambda: update_frame)
    else:
        on_closing()

with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)
camera_config = config_data['camera_config']

# 建立 RTSP 連線
#cap = cv2.VideoCapture(camera_config['local'])
cap = cv2.VideoCapture("rtsp://Admin:1234@192.168.7.21/cam0/h264")
####################
# tkinter
root = tk.Tk()
root.title("Monitor")

canvas = tk.Canvas(root, width=720, height=480)
canvas.pack()

# 結束按鈕
close_button = tk.Button(root, text="結束", command=on_closing)
close_button.pack()

# 定期更新畫面
update_frame()

# 關閉視窗的時候也執行 on_closing()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

# 釋放攝影機
cap.release()