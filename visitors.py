from base64 import b64encode
from datetime import datetime
from io import BytesIO
from os import listdir
from random import choice, randint
from socket import gethostbyname, gethostname
from uuid import uuid4

import numpy
import requests
from PIL import Image
from faker import Faker  # fake data library

import login
import settings
import time

fake = Faker('ru_RU')

# requests = requests.Session()
# requests.trust_env = False
# token = login.create_token({settings.controller_ip})


def create_visitor(amount, counter=1, total_time=0):
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
                'car_number': f'{(settings.letter(2) + str(randint(100, 999)) + settings.letter(1) + str(randint(0o1, 199)))}',
                'email': f'{fake.unique.ascii_free_email()}',
                'comment': f'{fake.address()}',
                'banned': False}
        headers = {'Content-type': 'application/json',
                   'Authorization': f'Bearer {token}',
                   'Accept': 'text/plain',
                   'Host': f'{gethostbyname(gethostname())}',
                   'User-Agent': 'PostmanRuntime/7.34.0'}
        url = f'https://{settings.controller_ip}/api/v1/visitors'
        requests.post(url, json=body, headers=headers, verify=False)

        # Image selection and conversion

        size = 320, 320
        output = BytesIO()
        image_filename = open((settings.image_path + choice(listdir(settings.image_path))), 'rb')
        image = Image.open(image_filename)
        new_image = Image.new('RGBA', image.size, 'white')
        new_image.paste(image, (0, 0), image)
        image = new_image.convert('RGB')
        image = image.resize(size)
        image.save(output, format='JPEG', quality=80)
        encoded_string = b64encode(output.getvalue()).decode()

        #

        body = {'image_data': '',
                'uuid': f'{visitor_uuid}'}
        headers = {'Content-type': 'application/json',
                   'Authorization': f'Bearer {token}',
                   'Accept': 'text/plain',
                   'Host': f'{gethostbyname(gethostname())}',
                   'User-Agent': 'PostmanRuntime/7.34.0'}
        url = f'https://{settings.controller_ip}/api/v1/images/'
        requests.post(url, json=body, headers=headers, verify=False)

        # Send user image

        body = {'image_data': f'data:image/jpeg;base64,{encoded_string}',
                'uuid': f'{visitor_uuid}'}
        url = f'https://{settings.controller_ip}/api/v1/images/{visitor_uuid}'
        requests.put(url, json=body, headers=headers, verify=False)
        elapsed_time = round((time.time() - start_time), 2)
        total_time = round((total_time + elapsed_time), 2)
        print(f'Created {counter} visitor out of {amount}, {firstname} {middle_name} {lastname} UUID [{visitor_uuid}], '
              f'creation time {elapsed_time} sec.')

        if amount == counter:
            print(f'\nTime elapsed: {total_time} sec.')
        else:
            pass

        counter += 1


# create_visitor(10)
