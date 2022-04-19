from random import randrange

import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


# импорт функций из модуля userinfo
import userinfo
import vk_token  # токен из отдельного файла

# токен удалить перед публикацией
token = vk_token.token
# token = input('Token: ')

vk = vk_api.VkApi(token=token)  # открывается сессия по токену
longpoll = VkLongPoll(vk)

# подопытные кролики

# user_id = 62117789  # me
# user_id = 1794202  # Julia
# user_id = 23212039  # Stepunn


hi_msg = ('Привет', 'привет')
message = 'Привет, username!'


def write_msg(user_id, message):
    rnd = randrange(10 ** 7)
    print(rnd)
    print(message)
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': rnd})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request in hi_msg:
                write_msg(event.user_id, f"Хай, {event.user_id}")
                if userinfo.main_user_byear() is None:
                    write_msg(event.user_id, 'сколько тебе лет?')
                    if userinfo.main_user_city() is None:
                        write_msg(event.user_id, 'Из какого ты города?')

            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "А я не пОняла!..")



msg = 'Привет, username'
# write_msg(user_id, msg)
