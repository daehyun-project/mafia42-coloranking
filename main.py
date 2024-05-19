import requests
import warnings
warnings.filterwarnings(action='ignore')

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
@app.get("/")
async def read_root():
    return "This is root path from MyAPI"
@app.get("/datas")
async def read_datas():
    return main()


# 요청을 숨기기 위함
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
}


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return r, g, b


def calculate_black_closeness(r, g, b):
    brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
    black_closeness = (1 - brightness) * 100

    return black_closeness


def main():
    url = "https://mafia42.com/comment/show-lastDiscussion"
    payload = {
        "comment": {
            "article_id": "1007550",
            "value": 0
        }
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    data = response.json()
    data = data['commentData']
    user_data = []
    for i in data:
        color = i['nickname_color']
        unsigned_value = color & 0xFFFFFFFF
        hex_value = hex(unsigned_value)
        formatted_hex_value = hex_value.upper().replace('0XFF', '')

        r, g, b = hex_to_rgb(formatted_hex_value)
        closeness = calculate_black_closeness(r, g, b)
        closeness = round(closeness, 2)

        s = {
            'nickname': i['nickname'],
            'color': formatted_hex_value,
            'closeness': closeness
        }
        user_data.append(s)

    user_data.sort(key=lambda x: x['closeness'], reverse=True)
    return user_data
