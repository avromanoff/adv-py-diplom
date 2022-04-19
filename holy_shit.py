from pprint import pprint
import re
from random import randrange

import requests
import vk_api
import vk_token  # токен из отдельного файла
from vk_api.longpoll import VkLongPoll, VkEventType


token = vk_token.token
access_token = vk_token.access_token
# token = input('Token: ')

test_user_id = 1  # Дуров
# test_user_id = 62117789  # me
# test_user_id = 1794202  # Julia
# test_user_id = 23212039  # Stepunn

main_user_byear = 1981  # год рождения юзера
main_user_sex = 2  # пол юзера
main_user_relation = 0  # отношения юзера
main_user_city_id = 2  # город юзера



relation_dict = {'1': 'не женат/не замужем',
                 '2': 'есть друг/есть подруга',
                 '3': 'помолвлен/помолвлена',
                 '4': 'женат/замужем',
                 '5': 'всё сложно',
                 '6': 'в активном поиске',
                 '7': 'влюблён/влюблена',
                 '8': 'в гражданском браке',
                 '0': 'Не указано'
                 }

sex_dict = {1: 'F', 2: 'M', 0: 'N/A', }


# запрашиваем сведения о пользователе по ID: дату рождения, пол, семейное положение, город)
# response = vk.method('users.get', {'user_ids': test_user_id, 'fields': 'bdate, birth_year, sex, relation, city'})[0]

# pprint(response[0])  # потом удалить
# print('id, byear, sex, relation, city_id, city_title')

# def response(user_id):
#     response = vk.method('users.get', {'user_ids': user_id, 'fields': 'bdate, birth_year, sex, relation, city'})
#     return response

# print(response)

vk = vk_api.VkApi(token=token)  # открывается сессия по токену


def main_user_data(user_id):
    # функция для получения сведений о текущем пользователе
    # (с которым ведется диалог)
    # словарь: id, год рождения, пол (код), отношения, id города, название города
    # если каких-то данных нет, то возвращается None
    # list.insert(i, x) - вставляет на i-ю позицию элемент x - NB, когда вставлять запрошенные значения
    userdata = {'user_id': user_id}
    # vk = vk_api.VkApi(token=token)  # открывается сессия по токену
    response = vk.method('users.get', {'user_ids': user_id, 'fields': 'bdate, sex, relation, city'})
    try:
        bdate = response[0]['bdate']
    except KeyError:
        user_byear = None
    else:
        year = re.search('[0-9]{4}', bdate)
        user_byear = year[0] if year else None  # если нет года рождения, тоже возвращается None
    userdata['user_byear'] = user_byear
    try:
        sex = response[0]['sex']
    except KeyError:
        sex = None
    userdata['sex'] = sex
    try:
        relation = response[0]['relation']
    except KeyError:
        relation = None
    userdata['relation'] = relation
    try:
        city = response[0]['city']
    except KeyError:
        # print('no city data')  # нужно будет спросить у пользователя, при запросе переводить 1й символ в UpperCase
        city = None
    # print(city)
    # print(city['id'])
    userdata['city_id'] = city['id']
    userdata['city_title'] = city['title']
    return userdata


def search_users_data():
    # ищет пользователей с данными, как у текущего пользователя,
    # удаляет закрытые акки,
    # извлекает 3 самые популярные (лакки + комменты) фотки профиля
    vk = vk_api.VkApi(token=access_token)  # сессия с токеном пользователя
    params = {'sort': 1, 'offset': offset, 'city': main_user_city_id, 'status': main_user_relation, 'sex': main_user_sex, 'birth_year': main_user_byear}
    users_response = vk.method('users.search', params)

    # удаляем закрытые аккаунты - переписываем открытые в новый список
    open_users_list = []
    for user in users_response['items']:
        if user['is_closed'] is False:
            open_users_list.append(user)

    print(f"всего нашлось {len(users_response['items'])}")

    for user in open_users_list:
        # print(user)
        owner_id = user['id']
        # owner_id = 62117789
        # получаем фото профиля каждого пользователя
        response = vk.method('photos.get', {'owner_id': owner_id, 'album_id': 'profile', 'extended': 1})
        # print(response['items'])
        # pprint(response['items'])
        count_userpics = response['count']
        print(f"Всего фотографий у пользователя {owner_id} -- {count_userpics}")
        if count_userpics == 0:
            best_photos = 'У пользователя нет фото'
        else:
            photos_info = {}
            for photos in response['items']:
                photo_id = photos['id']
                photo_likes = photos['likes']['count'] + photos['comments']['count']
                photo_url = 'https://vk.com/photo' + str(owner_id) + '_' + str(photo_id)
                photos_info[photo_id] = (photo_likes, photo_url)
            sorted_photos_info = sorted(photos_info.values(), reverse=True)  # сортировка в обратном порядке
            best_photos_count = min(3, count_userpics)
            best_photos = sorted_photos_info[:best_photos_count]
        # print(best_photos)
    return best_photos


print(main_user_data(test_user_id))

if main_user_data(test_user_id)['user_byear'] is None:
    print('Нужно спрашивать год рождения')

if main_user_data(test_user_id)['city_title'] is None:
    print('Нужно спрашивать город')

offset = 0  # пока используется в search_users_data()
# pprint(search_users_data())
# print(len(search_users_data()['items']))

# for user in search_users_data()['items']:
#     print(user['id'])
search_users_data()


