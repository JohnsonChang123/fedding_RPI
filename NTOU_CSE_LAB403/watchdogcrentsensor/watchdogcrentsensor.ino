#include "WiFiS3.h"
#include "EmonLib.h" 
#include "MySQL_Connection.h"
#include "MySQL_Cursor.h"

//////////////////////////////
const int ACPin = 1;

#define database 6 //資料庫ID
#define ACrange 30  //電流開關閥值


IPAddress server_addr(,,,);  // IP of the MySQL *server* here
char user[] = "lab403";              // MySQL user login username
char password[] = "66386638";        // MySQL user login password
int status = WL_IDLE_STATUS;
// WiFi card example
char ssid[] = "LIYE24";    // your SSID
char pass[] = "66386638";       // your SSID Password

WiFiClient client;            // Use this for WiFi instead of EthernetClient
MySQL_Connection conn((Client *)&client);

EnergyMonitor emon1;  


double  currentACC=0;
unsigned long previousMillis = 0;
const long ACCinterval = 300000;  // 設定每 300 秒更新一次資料庫
double ACCurrentValue=0;
/* -------------------------------------------------------------------------- */
void setup()
{
  /* -------------------------------------------------------------------------- */
  Serial.begin(115200);
  
  emon1.current(ACPin, 111.1); 


  
  while (!Serial){; }

  int temp_i=10;
  while(temp_i>0){
    ACCurrentValue = emon1.calcIrms(1480);// Calculate 電流 only
    temp_i--;
    delay(100);
  }


Serial.println("\n_____________RESTAR WIFI______________");
  while (status != WL_CONNECTED){
        Serial.print("Attempting to connect to SSID: ");
        Serial.println(ssid);
        status = WiFi.begin(ssid, pass);

        delay(500);
        }

  Serial.println("\n_____________RESTAR______________");
  temp_i=0;
  while (!conn.connect(server_addr, 3306, user, password)) {
        delay(500);
        if(temp_i>5){NVIC_SystemReset();}
        temp_i++;
      }

}

// Sample query
//char INSERT_SQL[] = "INSERT INTO test_arduino.hello_arduino (message) VALUES ('Hello, Arduino!')";
//UPDATE fishDB.feedalive SET time=NOW(),voltage=ACCurrentValue WHERE id=1;
/* -------------------------------------------------------------------------- */
void loop(){
/* -------------------------------------------------------------------------- */
  unsigned long currentMillis = millis();
  MySQL_Cursor *cur_mem = new MySQL_Cursor(&conn);
  ACCurrentValue = emon1.calcIrms(1480);// Calculate 電流 only




  // Initiate the query class instance
  if (currentMillis - previousMillis >= ACCinterval  || abs(currentACC-ACCurrentValue)  >15) {  //每過N秒 or 開關電 上傳資料
    Serial.print("abs(currentACC-ACCurrentValue): ");
    Serial.println(abs(currentACC-ACCurrentValue));
    previousMillis = currentMillis;
    currentACC=ACCurrentValue;

    char update_SQL[100];
    sprintf(update_SQL, "INSERT INTO fishDB.feed_alive (time, voltage) VALUES (CONVERT_TZ(NOW(), '+00:00', '+00:00') , %.2f);", ACCurrentValue);
    
    sprintf(update_SQL, "INSERT INTO ar0DB.feed_alive (time, voltage) VALUES (CONVERT_TZ(NOW(), '+00:00', '+00:00') , %.2f);", ACCurrentValue);
    cur_mem->execute(update_SQL);
    Serial.print("ACCurrentValue: ");
    Serial.println(ACCurrentValue);

  }
  
    if(ACCurrentValue>ACrange){
      char *update_mode_SQL="UPDATE ar0DB.cloud_config SET feed_alive = 1 WHERE id = 1";
      cur_mem->execute(update_mode_SQL);
      Serial.println("啟動觀察者模式");
    }
    else{
      char *update_mode_SQL="UPDATE ar0DB.cloud_config SET feed_alive = 0 WHERE id = 1";
      cur_mem->execute(update_mode_SQL);
      //      #Serial.println("關閉");
    }

      
    
 
    delete cur_mem;
    
    if (!conn.connected()){NVIC_SystemReset();}

    delay(1000);

}
