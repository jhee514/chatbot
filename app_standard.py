from flask import Flask, render_template, request
import requests
from decouple import config

app = Flask(__name__)

api_url = 'https://api.telegram.org'
token = config('TOKEN')
admin_id = config('ADMIN_ID')
secret_url = config('SECRET_URL')
naver_client_id = config('NAVER_CLIENT_ID')
naver_client_secret = config('NAVER_CLIENT_SECRET')

commands = [
    '/번역 <키워드>',
    '/미세먼지',
]


@app.route(f'/{secret_url}', methods=['POST'])
def telegram():
    req = request.get_json()
    user = req['message']['from']['id']  # user 의 chat id
    message = req['message']['text']  # user 의 입력 메시지
    no_error = '존재하지 않는 명령어 입니다.'

    if message[0] == '/':
        if ' ' in message:  # 띄어쓰기 후에 추가 input 있음
            words = message.split(' ')  # ['/번역', '띵작']
            if words[0] == '/번역':
                headers = {
                    'X-Naver-Client-Id': naver_client_id,
                    'X-Naver-Client-Secret': naver_client_secret,
                }

                data = {
                    'source': 'ko',
                    'target': 'en',
                    'text': words[1],
                }

                res = requests.post('https://openapi.naver.com/v1/papago/n2mt', data=data, headers=headers)
                result = res.json()['message']['result']['translatedText']  # 번역 결과
            
            else:
                result = no_error
        else:  # 띄어쓰기 없음
            if message == '/미세먼지':
                result = '좋음'
            else:
                result = no_error
    else:
        result = str(commands)



    URL = f'{api_url}/bot{token}/sendMessage?chat_id={user}&text={result}'
    requests.get(URL)
    return ('success', 200)

if __name__ == '__main__':
    app.run(debug=True, port=80)
