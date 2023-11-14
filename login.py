import requests
import settings
from warnings import filterwarnings

requests = requests.Session()
requests.trust_env = False


def create_token(controller_ip):
    filterwarnings('ignore')
    url = f'https://{settings.controller_ip}/api/v1/login'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'User-Agent': 'PostmanRuntime/7.34.0'}
    body = {"login": "admin", "password": "abc12345"}
    request = requests.post(url, json=body, headers=headers, verify=False)
    return request.json().get('token')

    # print(f'\nAccess token: {create_token(settings.controller_ip)}')
