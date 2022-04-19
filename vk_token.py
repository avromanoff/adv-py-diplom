token = '==='
access_token = '***'

http_token = 'https://oauth.vk.com/blank.html#access_token=***&expires_in=86400&user_id=62117789'

# получить токен пользователя (приложение -- vk.com) на https://vkhost.github.io/
# из полученной строки извлечь токен


import re

text = http_token

m = re.search('#access_token=(.+?)&expires_in', text)
if m:
    find = m.group(1)

print(find)
