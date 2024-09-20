import requests
import time
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiYnlyIiwiZXhwIjoxNzM2ODI2Nzk2fQ.57_-J8mHgolfmn_EPjnMwtmjW8YEAkEbGi3qheG-gdI"
cnt = 0
code = ""
headers = {
    'Authorization': f'Bearer {token}',
}
headers2 = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/x-www-form-urlencoded',
}
while(1):
    time.sleep(2)
    response = requests.get('http://127.0.0.1:1323/api/info', headers=headers)
    
    if response.status_code == 200:
        if code == response.json()["code"]:
            continue
        else:
            code = response.json()["code"]
            data = {
                'code':code
            }
            while(1):
                response2 = requests.post('http://127.0.0.1:1323/api/validate', headers=headers2, data=data)
                if response2.status_code == 200:
                    break
            cnt += 1
            print(f'{cnt} : {code}')
    
