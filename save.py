import json

import requests
import warnings

warnings.filterwarnings(action='ignore')

def saveUser():
    headers = {
        "Content-Type": "application/json"
    }

    main_url = "https://mafia42.com/api/show-lastDiscussion/1007550"
    response = requests.get(main_url, headers=headers)

    response = response.json()
    response = response['boardData']
    data = response['comment_count']

    n = (data // 30) + 1

    url = "https://mafia42.com/comment/show-lastDiscussion"
    payload = {
        "comment": {
            "article_id": "1007550",
            "value": 0
        }
    }

    user_data = {}

    for _ in range(0, n):
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        data = data['commentData']
        for i in data:
            try:
                url2 = "https://mafia42.com/api/user/user-info"
                user_id = {'id': i['user_id']}

                data2 = requests.post(url2, json=user_id, headers=headers).json()
                data2 = data2['userData']

                user_data[data2['NICKNAME']] = {
                    'ID': data2['ID'],
                    'GAMES': data2['win_count'] + data2['lose_count']}

                # user_data.append()
            except:
                pass
        payload['comment']['value'] += 30

    with open('data2.json', 'w', encoding='UTF-8-sig') as f:
        f.write(json.dumps(user_data, ensure_ascii=False))

saveUser()