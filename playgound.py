from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests, bs4, json, time
 
data =  {"post_id": 160187,
		 "file_name": 'Speed Racer (Europe) (En,Fr,De,Es,It,Nl).7z',
		 "server_id": 4}
data_json = json.dumps(data)
headers = {'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
response = requests.post("https://cdromance.com/wp-content/plugins/cdromance/public/direct.php", data=data_json, headers=headers)
print(response.text)