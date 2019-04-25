from flask import Flask, request
import logging
import requests
# библиотека, которая нам понадобится для работы с JSON
import json


def get_post(num):
    texts = []
    req = 'https://api.vk.com/method/wall.get'
    response = requests.get(
        'https://api.vk.com/method/wall.get?owner_id=-112510789&count=100&access_token=b346d612b346d612b346d61288b32cfdcebb346b346d612eff9ea604f19d70c363f4e13&v=5.95')
    text = response.json()['response']['items'][num]['text']
    print(text)
    return text


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/', methods=['POST'])
# Функция получает тело запроса и возвращает ответ.
# Внутри функции доступен request.json - это JSON,
# который отправила нам Алиса в запросе POST
def main():
    logging.info('Request: %r', request.json)

    # Начинаем формировать ответ, согласно документации
    # мы собираем словарь, который потом при помощи библиотеки json
    # преобразуем в JSON и отдадим Алисе
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    # Отправляем request.json и response в функцию handle_dialog.
    # Она сформирует оставшиеся поля JSON, которые отвечают
    # непосредственно за ведение диалога
    handle_dialog(request.json, response)

    logging.info('Response: %r', request.json)

    # Преобразовываем в JSON и возвращаем
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'number': 1
        }
        # Заполняем текст ответа
        res['response'][
            'text'] = 'Привет! Здесь ты можешь увидеть актуальные новости . Все новости, которые ты видишь мы берем из портала MASH вот ссылка https://vk.com/mash'
        return

    if req['request']['original_utterance'].lower() in [
        'хочу получить новости',
        'актуальные новости',
        'хочу новость',
        'новость',
        'хочу новости'
    ]:
        print(sessionStorage[user_id]['number'])
        if get_post(sessionStorage[user_id]['number']) != '':
            res['response']['text'] = get_post(sessionStorage[user_id]['number'])
            sessionStorage[user_id]['number'] += 1
            print(res['response']['text'])
            return
        else:
            res['response']['text'] = get_post(sessionStorage[user_id]['number']+1)
            sessionStorage[user_id]['number'] += 2
            print(res['response']['text'])
            return
    elif req['request']['original_utterance'] == 'ещё' and sessionStorage[user_id]['number'] >= 2:
        if get_post(sessionStorage[user_id]['number']) != '':
            res['response']['text'] = get_post(sessionStorage[user_id]['number'])
            sessionStorage[user_id]['number'] += 1
            print(res['response']['text'])
            return
        else:
            res['response']['text'] = get_post(sessionStorage[user_id]['number'] + 1)
            sessionStorage[user_id]['number'] += 2
            print(res['response']['text'])
            return

    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = 'я не понимаю данной команды'
