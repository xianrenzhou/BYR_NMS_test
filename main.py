import time
import requests
class nmsclint(object):
    
    def __init__(self,username = "byr"):
        self.username = username
        self.url = "http://127.0.0.1:1323/"
        self.user_info = {}
        self.token = {}
        self.headers = {}
        self.cnt = 0
        self.code = ""

    def my_sleep(self,sleep_times=5):
        for i in range(sleep_times):
            print(f"sleep {sleep_times-i}s")
            time.sleep(1)

    
    def sign_up(self):
        '''
        注册 若失败，五秒后重试
        '''
        print("sign_up...")
        signup_url = self.url + "signup"
        data = {'username': self.username}
        while True:
            try:
                response = requests.post(signup_url, json=data)
                if response.status_code == 200:
                    break
                else:
                    print(f"Sign-up error: {response.status_code}")
            except requests.RequestException as e:
                print(f"Sign-up failed due to network error: {e}")
            self.my_sleep(sleep_times=10)
        try:
            self.user_info = response.json()
        except ValueError:
            print("Error parsing sign-up response as JSON")
        print("sign up success!")

    def login(self):
        '''
        登录 若失败，10秒后重试
        '''
        print("login...")
        login_url = self.url + "login"
        data = self.user_info
        while True:
            try:
                response = requests.post(login_url, data)
                if response.status_code == 200:
                    print("Login successful")
                    break
                else:
                    print(f"Login error: {response.status_code}")
            except requests.RequestException as e:
                print(f"Login failed due to network error: {e}")
            self.my_sleep(10)
        self.update_headers(response)
        
    
    def update_headers(self,response):
        print("update_headers")
        try:
            self.token = response.json()
            self.headers = {'Authorization': 'Bearer ' + self.token["token"]}
            print(f'Headers updated: {self.headers}')
        except ValueError:
            print("Error parsing login response as JSON")
        

    def heart_beat(self):
        '''
        心跳+出错重连
        '''
        print("heart_beat")
        heart_url = self.url + "api/heartbeat"
        while True:
            try:
                response = requests.get(heart_url, headers=self.headers)
                if response.status_code == 200:
                    print("Request successful!")
                    self.update_headers(response)
                    break
                elif response.status_code == 401 or response.status_code == 500:
                    print("Unauthorized or server error, trying to log in...")
                    self.login()
                    break  
                else:
                    print(f"Error code (GET): {response.status_code}")
            except requests.RequestException as e:
                print(f"Request failed due to network error: {e}")
            self.my_sleep(3)
        
        
    
    def get_info(self):
        print("get_info")
        info_url =  self.url + "api/info"
        while True:
            try:
                response = requests.get(info_url, headers=self.headers)
                if response.status_code == 200:
                    if response.json()["code"] == self.code:
                        self.my_sleep(10)
                        continue
                    else:
                        self.code = response.json()["code"]
                        break
                else:
                    print(f"Error code (GET): {response.status_code}")   
            except requests.RequestException as e:
                print(f"Request failed due to network error: {e}")
            self.heart_beat()


    def submit_info(self):
        print("submit info")
        val_url = self.url+"api/validate"
        while True:
            headers = self.headers
            headers["Content-Type"] = 'application/x-www-form-urlencoded'
            data = {'code':self.code}
            try:
                response = requests.post(val_url, headers=headers, data=data)
                if response.status_code == 200:
                    self.cnt += 1
                    print(f'code:{self.code}提交成功，当前共提交{self.cnt}个code！')
                    break
                else:
                    print(f"Error code (GET): {response.status_code}")   
                
            except  requests.RequestException as e:
                print(f"Request failed due to network error: {e}")
            self.heart_beat()
                
    
    def error_process(self,errorcode):

        print("error process")

nms = nmsclint()
nms.sign_up()
nms.login()
while(1):
    time.sleep(3)
    nms.get_info()
    nms.submit_info()
    # print(nms.cnt)