from flask import Flask, request
import logging
import requests
# библиотека, которая нам понадобится для работы с JSON
import json


def get_post(num, group=1):
    if group == 1:
        req = 'https://api.vk.com/method/wall.get'
        response = requests.get(
            'https://api.vk.com/method/wall.get?owner_id=-112510789&count=20&access_token=b346d612b346d612b346d61288b32cfdcebb346b346d612eff9ea604f19d70c363f4e13&v=5.95')
        text = response.json()['response']['items'][num]['text']
    if group == 2:
        req = 'https://api.vk.com/method/wall.get'
        response = requests.get(
            'https://api.vk.com/method/wall.get?owner_id=-29534144&count=20&access_token=b346d612b346d612b346d61288b32cfdcebb346b346d612eff9ea604f19d70c363f4e13&v=5.95')
        text = response.json()['response']['items'][num]['text']
    if group == 0:
        req = 'https://api.vk.com/method/wall.get'
        response = requests.get(
            'https://api.vk.com/method/wall.get?owner_id=-145037861&count=20&access_token=b346d612b346d612b346d61288b32cfdcebb346b346d612eff9ea604f19d70c363f4e13&v=5.95')
        text = response.json()['response']['items'][num]['text']
    return text


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}

text = 'Привет! Здесь ты можешь увидеть актуальные новости .' \
       ' Все новости, которые ты видишь мы берем из порталов MASH ' \
       ', Сталингулаг ,Лентач. Ссылки на источники новостей : https://vk.com/mash \n' \
       'https://vk.com/oldlentach \n ' \
       'https://vk.com/stalingulag'

help = 'И снова здравствуй! Ниже указан список всех команд. \n' \
       'Для получения новости используются даннные команды:\n' \
       'Хочу получить новости; \n' \
       'Актуальные новости; \n' \
       'Новость; \n' \
       'Хочу новости.\n' \
       'Для получения последующих новостей используется команда "ещё".\n' \
       'Для того , чтобы поменять источник новостей используются следнующие команды: \n' \
       'Сменить источник новостей;\n' \
       'Другой источник.\n' \
       'Удачи!'
what_i_can = 'Я могу отсылать интересные новости)'


@app.route('/', methods=['POST'])
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
            'number': 1,
            'news_parser': 1
        }
        # Заполняем текст ответа
        res['response']['text'] = text
        res['response']['buttons'] = get_suggests(user_id)
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
            res['response']['text'] = get_post(sessionStorage[user_id]['number'],
                                               sessionStorage[user_id]['news_parser'] % 3)
            sessionStorage[user_id]['number'] += 1
            res['response']['buttons'] = get_suggests(user_id)
            print(res['response']['text'])
            return
        else:
            res['response']['text'] = get_post(sessionStorage[user_id]['number'] + 1,
                                               sessionStorage[user_id]['news_parser'] % 3)
            sessionStorage[user_id]['number'] += 2
            res['response']['buttons'] = get_suggests(user_id)
            print(res['response']['text'])
            return
    elif req['request']['original_utterance'].lower() == 'ещё' and sessionStorage[user_id]['number'] >= 2:
        if get_post(sessionStorage[user_id]['number']) != '':
            res['response']['text'] = get_post(sessionStorage[user_id]['number'],
                                               sessionStorage[user_id]['news_parser'] % 3)
            sessionStorage[user_id]['number'] += 1
            res['response']['buttons'] = get_suggests(user_id)
            print(res['response']['text'])
            return
        else:
            res['response']['text'] = get_post(sessionStorage[user_id]['number'] + 1,
                                               sessionStorage[user_id]['news_parser'] % 3)
            sessionStorage[user_id]['number'] += 2
            res['response']['buttons'] = get_suggests(user_id)
            print(res['response']['text'])
            return
    elif req['request']['original_utterance'].lower() in ['сменить источник новостей', 'другой источник', 'сменить новости']:
        sessionStorage[user_id]['news_parser'] += 1
        sessionStorage[user_id]['number'] = 1
        res['response']['buttons'] = get_suggests(user_id)
        res['response']['text'] = 'Теперь новости берутся из другого источника'
        return
    elif req['request']['original_utterance'].lower() in ['помощь']:
        res['response']['buttons'] = get_suggests(user_id)
        res['response']['text'] = help
        return
    elif req['request']['original_utterance'].lower() in ['что я могу']:
        res['response']['buttons'] = get_suggests(user_id)
        res['response']['text'] = what_i_can
        return

        # Если нет, то убеждаем его купить слона!
    res['response']['text'] = 'я не понимаю данной команды'


def get_suggests(user_id):
    if sessionStorage[user_id]['number'] >= 2:
        buttons = [{'title': 'Ещё', 'hide': False},
                   {'title': 'Сменить новости', 'hide': False},
                   {'title': 'Помощь', 'hide': False},
                   {'title': 'Что я могу', 'hide': False}]
    else:
        buttons = [{'title': 'Хочу новость', 'hide': False},
                   {'title': 'Сменить источник новостей', 'hide': False},
                   {'title': 'Помощь', 'hide': False},
                   {'title': 'Что я могу', 'hide': False}]
    return buttons
