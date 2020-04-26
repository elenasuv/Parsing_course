import requests
import json
username = 'elenasuv'

main_link = 'https://api.github.com/users/' + username + '/repos'

response = requests.get(main_link, verify = False)

if response.ok:
    data = response.json()

print(f'У пользователя {username} следующие репозитории: {", ".join([i["name"] for i in data])}')
