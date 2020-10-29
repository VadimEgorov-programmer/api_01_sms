import logging
import time
import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()
VK_TOKEN = os.getenv('token')
VK_API_V = '5.124'
URL = 'https://api.vk.com/method/users.get'
GET_USER = 'users.get'
ACC_SID = os.getenv('account_sid')
AUTH_TOKEN = os.getenv('auth_token')
NUMBER_FROM = os.getenv('NUMBER_FROM')
NUMBER_TO = os.getenv('NUMBER_TO')
client = Client(ACC_SID, AUTH_TOKEN)


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'fields': 'online',
        'v': VK_API_V,
        'access_token': VK_TOKEN
    }
    url = URL + GET_USER
    try:
        request = requests.post(url, params=params).json()['response']
        user_status = request[0]['online']
        return user_status
    except Exception as e:
        logging.exception(f"Error: {e}")


def sms_sender(sms_text):
    message = client.messages.create(
        body=sms_text,
        from_=NUMBER_FROM,
        to=NUMBER_TO,
    )
    return message.sid


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
