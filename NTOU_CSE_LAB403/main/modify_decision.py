import mysql.connector
import sys
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

# 插入資料
def insert_data(data):
    query = "INSERT INTO decision (id, mode, angle, period, amount, fetch_interval) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (data['id'], data['mode'], data['angle'], data['period'], data['amount'], data['fetch_interval'])
    mycursor.execute(query, values)
    fishDB.commit()

# 查詢資料
def select_data():
    query = "SELECT * FROM decision WHERE id = 1"
    mycursor.execute(query)
    result = mycursor.fetchall()
    return result

# 更新資料
def update_data(data):
    query = "UPDATE decision SET mode = %s, angle = %s, period = %s, amount = %s, fetch_interval = %s WHERE id = 1"
    values = (data['new_mode'], data['new_angle'], data['new_period'], data['new_amount'], data['new_interval'])
    mycursor.execute(query, values)
    fishDB.commit()

# 刪除資料
def delete_data(id):
    query = "DELETE FROM decision WHERE id = %s"
    value = (id,)
    mycursor.execute(query, value)
    fishDB.commit()

# 關閉資料庫連線
def close_connection():
    mycursor.close()
    fishDB.close()

# 使用範例
if __name__ == "__main__":
    try:
        delete_data(1)
        #inserted_data = {'id': sys.argv[1], 'mode': sys.argv[2], 'angle': sys.argv[3], 'period': sys.argv[4], 'amount': sys.argv[5], 'fetch_interval': sys.argv[6]}
        inserted_data = {'id': 1, 'mode': 3, 'angle': 30, 'period': 999, 'amount': 100, 'fetch_interval': 3}
        insert_data(inserted_data)
        #updated_data = {'new_mode': sys.argv[1], 'new_angle': sys.argv[2], 'new_period': sys.argv[3], 'new_amount': sys.argv[4], 'new_interval': sys.argv[5]}
        #update_data(updated_data)
        #delete_data(1)

    except Exception as e:
        print("An error occurred:", e)
    finally:
        close_connection()

'''
把 decision 裡 id = 1 的地方先 delete 再 insert
在指令內容出現異常時，直接重設一個值讓指令格式恢復正常。
'''