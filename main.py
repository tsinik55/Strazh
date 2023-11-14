from base64 import b64encode
from datetime import datetime, timedelta
from io import BytesIO
from os import listdir
from random import choice, randint
from socket import gethostbyname, gethostname
from uuid import uuid4

import numpy
from PIL import Image
from faker import Faker  # fake data library
import time

fake = Faker('ru_RU')

import requests
import settings as s
from warnings import filterwarnings

controller_ip = '172.16.132.13'
controller_id = '00000097'
image_path = '.\\Spotty\\'

requests = requests.Session()
requests.trust_env = False


def letter(amount):
    char = ''
    for _ in range(amount):
        char += choice('ABEKMHOPCTYX')
    return char


def create_token(controller_ip):
    filterwarnings('ignore')
    url = f'https://{s.controller_ip}/api/v1/login'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'User-Agent': 'PostmanRuntime/7.34.0'}
    body = {"login": "admin", "password": "abc12345"}
    request = requests.post(url, json=body, headers=headers, verify=False)
    token = request.json().get('token')
    print(f'\nAccess token: {token}')
    return token


def create_visitor(amount, counter=1, total_time=0):
    token = create_token(s.controller_ip)
    for _ in range(amount):
        start_time = time.time()
        current_time = int(time.mktime(datetime.now().timetuple()))
        visitor_uuid = uuid4()
        gender = numpy.random.choice(['male', 'female'], p=[0.5, 0.5])
        if gender == 'male':
            firstname = fake.first_name_male()
            middle_name = fake.middle_name_male()
            lastname = fake.last_name_male()
        else:
            firstname = fake.first_name_female()
            middle_name = fake.middle_name_female()
            lastname = fake.last_name_female()
        body = {'uuid': f'{visitor_uuid}',
                'phone': f'+79{fake.msisdn()[4:]}',
                'name': f'{firstname}',
                'second_name': f'{middle_name}',
                'surname': f'{lastname}',
                'company': f'{fake.company()}',
                'first_access': f'{current_time - randint(9999000, 99999000)}000',
                'last_access': f'{current_time - randint(9000, 1999000)}000',
                'status': choice(('WAITING', 'ACTIVE:INNER', 'ACTIVE:OUTER', 'BANNED', 'NOT-COME', 'ARCHIVE',
                                  'VIOLATION')),
                'car_number': f'{(letter(2) + str(randint(100, 999)) + letter(1) + str(randint(0o1, 199)))}',
                'email': f'{fake.unique.ascii_free_email()}',
                'comment': f'{fake.address()}',
                'banned': False}
        headers = {'Content-type': 'application/json',
                   'Authorization': f'Bearer {token}',
                   'Accept': 'text/plain',
                   'Host': f'{gethostbyname(gethostname())}',
                   'User-Agent': 'PostmanRuntime/7.34.0'}
        url = f'https://{controller_ip}/api/v1/visitors'
        requests.post(url, json=body, headers=headers, verify=False)

        create_userpic(visitor_uuid, token)

        elapsed_time = (time.time() - start_time)
        total_time = total_time + elapsed_time
        n_time = str(timedelta(seconds=total_time)).split(':')

        print(f'Created {counter} visitor out of {amount}, {firstname} {middle_name} {lastname} UUID [{visitor_uuid}], '
              f'creation time {round(elapsed_time, 2)} sec.')

        if amount == counter:
            print(f'\nTime elapsed: {n_time[0]} Hours {n_time[1]} Minutes {round(float(n_time[2]), 2)} Sec')
        else:
            pass
        counter += 1


def create_staff(amount, counter=1, total_time=0):
    token = create_token(controller_ip)
    for _ in range(amount):
        start_time = time.time()
        staff_uuid = uuid4()
        gender = numpy.random.choice(['male', 'female'], p=[0.5, 0.5])
        if gender == 'male':
            firstname = fake.first_name_male()
            middle_name = fake.middle_name_male()
            lastname = fake.last_name_male()
        else:
            firstname = fake.first_name_female()
            middle_name = fake.middle_name_female()
            lastname = fake.last_name_female()
        body = {'uuid': f'{staff_uuid}',
                'name': f'{firstname}',
                'second_name': f'{middle_name}',
                'surname': f'{lastname}',
                'car_number': f'{(letter(2) + str(randint(100, 999)) + letter(1) + str(randint(0o1, 199)))}',
                'email': f'{fake.unique.ascii_free_email()}',
                'access_profiles': [],
                'access_point': '',
                'cards': [],
                'pin': '',
                'biometry': {
                    'models': []
                },
                'comment': f'{fake.address()}',
                'banned': False}
        headers = {'Content-type': 'application/json',
                   'Authorization': f'Bearer {token}',
                   'Accept': 'text/plain',
                   'Host': f'{gethostbyname(gethostname())}',
                   'User-Agent': 'PostmanRuntime/7.34.0'}
        url = f'https://{controller_ip}/api/v1/staff'
        requests.post(url, json=body, headers=headers, verify=False)

        create_userpic(staff_uuid, token)

        elapsed_time = (time.time() - start_time)
        total_time = total_time + elapsed_time
        n_time = str(timedelta(seconds=total_time)).split(':')

        print(
            f'Created {counter} staff members out of {amount}, {firstname} {middle_name} {lastname} UUID [{staff_uuid}], '
            f'creation time {round(elapsed_time, 2)} sec.')

        if amount == counter:
            print(f'\nTime elapsed: {n_time[0]} Hours {n_time[1]} Minutes {round(float(n_time[2]), 2)} Sec')
        else:
            pass
        counter += 1


def create_userpic(uuid, token):
    size = 320, 320
    output = BytesIO()
    image_filename = open((image_path + choice(listdir(image_path))), 'rb')
    image = Image.open(image_filename)
    new_image = Image.new('RGBA', image.size, 'white')
    new_image.paste(image, (0, 0), image)
    image = new_image.convert('RGB')
    image = image.resize(size)
    image.save(output, format='JPEG', quality=80)
    encoded_string = b64encode(output.getvalue()).decode()
    body = {'image_data': '',
            'uuid': f'{uuid}'}
    headers = {'Content-type': 'application/json',
               'Authorization': f'Bearer {token}',
               'Accept': 'text/plain',
               'Host': f'{gethostbyname(gethostname())}',
               'User-Agent': 'PostmanRuntime/7.34.0'}
    url = f'https://{controller_ip}/api/v1/images/'
    requests.post(url, json=body, headers=headers, verify=False)

    # Send user image

    body = {'image_data': f'data:image/jpeg;base64,{encoded_string}',
            'uuid': f'{uuid}'}
    url = f'https://{controller_ip}/api/v1/images/{uuid}'
    requests.put(url, json=body, headers=headers, verify=False)


def create_identifier(user_uuid, ):
    token = create_token(controller_ip)
    identifier_uuid = uuid4()
    identifier_format = numpy.random.choice(['qr', 'barcode', 'card'])
    current_time = int(time.mktime(datetime.now().timetuple()))
    body = {
        'code': f'{identifier_uuid}',
        'privilege': '',
        'disposable': True,
        'no_expire_delete': True,
        'active_from': f'{current_time - randint(9999000, 99999000)}000',
        'active_to': f'{current_time + randint(199000, 1999000)}000',
        # 'first_access': f'{current_time - randint(9999000, 99999000)}000',
        # 'last_access': f'{current_time - randint(9000, 1999000)}000',
        'user_uuid': f'{user_uuid}',
        'comment': '',
        'format': f'{identifier_format}',
        'ext_privileges': ''
    }
    headers = {'Content-type': 'application/json',
               'Authorization': f'Bearer {token}',
               'Accept': 'text/plain',
               'Host': f'{gethostbyname(gethostname())}',
               'User-Agent': 'PostmanRuntime/7.34.0'}
    url = f'https://{controller_ip}/api/v1/identifiers'
    requests.post(url, json=body, headers=headers, verify=False)


create_identifier(1)

create_staff(1000)
# create_visitor(1)
