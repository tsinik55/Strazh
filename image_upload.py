import socket
import login
import requests
from uuid import uuid4
from base64 import b64encode
from os import listdir
from random import choice
from faker import Faker  # fake data library

import settings

fake = Faker('ru_RU')

requests = requests.Session()
requests.trust_env = False
token = login.create_token()



def userpic(uuid):
    userpic_filename = open((userpic_path + choice(listdir(userpic_path))), 'rb')
    # with open((userpic_path + choice(listdir(userpic_path))), 'rb') as userpic_filename:
    print(f'\n{userpic_filename}')
    userpic_encoded: bytes = b64encode(userpic_filename.read())
    # print(f'\n{userpic_encoded}')
    return userpic_encoded


def img_upload(uuid):
    userpic_filename = open((userpic_path + choice(listdir(userpic_path))), 'rb')

    # with open((userpic_path + choice(listdir(userpic_path))), 'rb') as userpic_filename:

    print(f'\n{userpic_filename}')
    userpic_encoded: bytes = b64encode(userpic_filename.read())

    # user_uuid = uuid4()

    body = {'uuid': f'{uuid}',
            'image_data': f'{userpic_encoded}'}
    headers = {'Content-type': 'application/json',
               'Authorization': f'Bearer {token}',
               'Accept': 'text/plain',
               'Host': f'{socket.gethostbyname(socket.gethostname())}',
               'User-Agent': 'PostmanRuntime/7.34.0'}
    url_del = f'https://{settings.controller_ip}/api/v1/images/{uuid}'  # Url for userpic deletion
    url_post = f'https://{settings.controller_ip}/api/v1/images'
    # requests.delete(url_del, headers=headers, verify=False)   # Request for userpic deletion
    requests.post(url_post, json=body, headers=headers, verify=False)


img_upload(uuid4)

#
# def img_upload():
#     for _ in range():
#         random_uuid = str'uuid4()'
#         body = {'uuid': f'{random_uuid}',
#             'image_data': f'{userpic_encoded}'
#         headers = {'Content-type': 'application/json',
#            'Authorization': f'Bearer {token}',
#            'Accept': 'text/plain',
#            'Host': f'{socket.gethostbyname(socket.gethostname())}',
#            'User-Agent': 'PostmanRuntime/7.34.0'}
#         url0 = f'https://{settings.ip}/api/v1/images/{random_uuid}'
#         url = f'https://{main.ip}/api/v1/images'
#         print(requests.delete(url0, headers=headers, verify=False))
#         print(requests.post(url, json=body, headers=headers, verify=False))
#
#         print(img_upload())
#
#
# def img_upload2():
#     body = {'uuid': f'1823ce5e-2234-43db-b31f-95a192b5b3d7',
#             'image_data': 'data:image/jpeg;base64,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'}
#     headers = {'Content-type': 'application/json',
#                'Authorization': f'Bearer {token}',
#                'Accept': 'text/plain',
#                'Host': f'{socket.gethostbyname(socket.gethostname())}',
#                'User-Agent': 'PostmanRuntime/7.34.0'}
#     url0 = f'https://{main.ip}/api/v1/images/1823ce5e-2234-43db-b31f-95a192b5b3d7'
#     url = f'https://{main.ip}/api/v1/images'
#     requests.delete(url0, headers=headers, verify=False)
#     requests.post(url, json=body, headers=headers, verify=False)
#
#
# img_upload()
