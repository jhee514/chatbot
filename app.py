from flask import Flask, render_template, request
import requests
from decouple import config

app = Flask(__name__)

api_url = 'https://api.telegram.org'
token = config('TOKEN')
# chat_id = config('CHAT_ID')
secret_url = config('SECRET_URL')
naver_client_id = config('NAVER_CLIENT_ID')
naver_client_secret = config('NAVER_CLIENT_SECRET')

commands = [
    '/번역 <키워드>',
    '/미세먼지',
]


@app.route(f'/{secret_url}', methods=['POST'])
def telegram():
    req = request.get_json() # 이 정보가 나에게 온 메세지를 요청하는 것  # 여기 나온 정보에서 필요한건 id와 text뿐(그래야그에맞는응답을하지)
    user = req['message']['from']['id']  # 메세지 안에 프롬 안에 아이디를 뽑아내는것 #user의 chat id
    message = req['message']['text']  # user의 입력 메세지
    no_error = '존재하지 않는 명령어 입니다.'

    if message[0] =='/':
        if ' 'in message:  # 띄어쓰기 후에 추가 input 있음
            words = message.split(' ')  # ['/번역', '댕댕이']
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
                result = res.json()['message']['result']['translatedText']  # 번역결과
            else:
                result = no_error

        else:  # 띄어쓰기 없음
            if message == '/미세먼지':
                result = '좋음'
            else:
                result = no_error
    else:
        result = commands


    URL = f'{api_url}/bot{token}/sendMessage?chat_id={user}&text={result}'
    requests.get(URL)  # flask에서 텔레그램으로 메세지 보내라고 연락하는 것
    return ('success', 200)  # 텔레그램은 200을 꼭 보내줘야 회차가 종료된다, return 웹훅으로 잘 받았다고 메세지 보내는 것


@app.route('/write')
def write():
    return render_template('write.html')


@app.route('/send')
def send():
    message = request.args.get('message')
    # 'message'는 사용자 input 값이고 그 걸 message tag에 저장
    URL = f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={message}'
    requests.get(URL)
    return render_template('send.html', message=message)




if __name__ == '__main__':
    app.run(debug=True, port=80)
