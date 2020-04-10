import requests
import json

method_name = 'friends.getOnline'
main_link = 'https://api.vk.com/method/' + method_name
access_token = '26d1f2320cbca8895e5760141f40293b197ea7184fc9613eb350217c577e52247e79637cc58f9f3a36d81'

params = {
    'v': 5.52,
    'access_token':access_token
}

response = requests.get(main_link, params=params, verify=False)
id = 7930430
if response.ok:
    data = response.json()

print(f'У пользователя VK с ID = {id} ID друзей, находящихся онлайн, следующие: {", ".join([str(i) for i in data["response"]])}')
