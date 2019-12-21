
# coding: utf-8

# In[ ]:
import vk_api
import requests
import random
from bs4 import BeautifulSoup 
from vk_api.longpoll import VkLongPoll, VkEventType
def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})
token = '2510043a6191f2796a42b3c3c9a7e85ba77c66c2c5636d087fe3be87b97f8cdab271bdeac986eabfecfe5'
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            if request == "привет" or request == 'Привет':
                write_msg(event.user_id, """Привет, мой юный любитель искусства, я Надежда Викторовна, твой личный консультант по расписанию Малого театра, МХАТа и Ленкома. Напиши мне название театра и дату, когда ты хочешь его посетить. Например, "Малый театр 30.12.2019".""")
            elif request == "пока" or request == 'Пока':
                write_msg(event.user_id, "Рада была пообщаться")
            elif request[:len(request)-11] == 'МХАТ' or request[:len(request)-11] == 'Ленком':
                today = requests.get('http://www.xn--80aajbde2dgyi4m.xn--p1ai/')
                today = BeautifulSoup(today.text, "html.parser")
                today = today.find("p", id = "digital_date")
                today = today.getText()
                date = request[-10:-8]
                t = 0
                if request[-7:-5] == '01' and int(request[-10:-8]) <= 31:
                    date += 'Янв'
                elif request[-7:-5] == '02' and (int(request[-10:-8]) <= 28 and int(request[-4:]) % 4 != 0 or int(request[-10:-8]) <= 29 and int(request[-4:]) % 4 == 0):
                    date += 'Фев'
                elif request[-7:-5] == '03' and int(request[-10:-8]) <= 31:
                    date += 'Мар'
                elif request[-7:-5] == '04' and int(request[-10:-8]) <= 30:
                    date += 'Апр'
                elif request[-7:-5] == '05' and int(request[-10:-8]) <= 31:
                    date += 'Май'
                elif request[-7:-5] == '06' and int(request[-10:-8]) <= 30:
                    date += 'Июн'
                elif request[-7:-5] == '07' and int(request[-10:-8]) <= 31:
                    date += 'Июл'
                elif request[-7:-5] == '08' and int(request[-10:-8]) <= 31:
                    date += 'Авг'
                elif request[-7:-5] == '09' and int(request[-10:-8]) <= 30:
                    date += 'Сен'
                elif request[-7:-5] == '10' and int(request[-10:-8]) <= 31:
                    date += 'Окт'
                elif request[-7:-5] == '11' and int(request[-10:-8]) <= 30:
                    date += 'Ноя'
                elif request[-7:-5] == '12' and int(request[-10:-8]) <= 31:
                    date += 'Дек'
                else:
                    t = 1
                if t == 1:
                    write_msg(event.user_id, "То ли ты не то написал, то ли я не так поняла. Может, попробуем ещё раз?")
                else:
                    if int(request[-4:]) > int(today[-4:]) and (int(request[-7:-5]) > int(today[3:5]) or int(request[-7:-5]) == int(today[3:5]) and int(request[-10:-8]) >= int(today[:2])):
                        write_msg(event.user_id, "Прошу прощения, я не вижу так далеко. Как говорится, близорукость не порок")
                    elif int(request[-4:]) < int(today[-4:]) or int(request[-4:]) == int(today[-4:]) and int(request[-7:-5]) < int(today[3:5]) or int(request[-4:]) == int(today[-4:]) and int(request[-7:-5]) == int(today[3:5]) and int(request[-10:-8]) < int(today[:2]):
                        write_msg(event.user_id, "Я помню это чудное мгновенье. Но прошлого не вернёшь. Может, посмотришь что-нибудь на будущее?")
                    if request[:len(request)-11] == 'МХАТ':
                        theatre = requests.get('https://mxat-teatr.com/afisha/')
                    elif request[:len(request)-11] == 'Ленком':
                        theatre = requests.get('https://len.theater/?utm_medium=cpc&utm_source=yandex&utm_campaign=obshaya_yandex&utm_term=%D0%BB%D0%B5%D0%BD%D0%BA%D0%BE%D0%BC%20%D1%82%D0%B5%D0%B0%D1%82%D1%80%20%D0%BE%D1%84%D0%B8%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%81%D0%B0%D0%B9%D1%82%20%D0%B0%D1%84%D0%B8%D1%88%D0%B0&utm_content=premium.1&utm_campaign_id=37966739&utm_group_id=3532701385&utm_term_id=14713448280&yclid=7554160873314737676')
                    else:
                        k = BeautifulSoup(theatre.text, "html.parser")
                        k1 = k.find_all("div", {"class": "ev_date"})
                        k2 = k.find_all("div", {"class": "date__text inline-top"})
                        k3 = k.find_all("div", {"class": "ev_date__time"})
                        n = 0
                        for i in range(len(k1)):
                            k1[i] = k1[i].getText()
                            k2[i] = k2[i].getText()
                            k3[i] = k3[i].getText()
                            if k1[i][:5] == date:
                                n = 1
                                k2[i] = k2[i].replace('  ', '')
                                k2[i] = k2[i].replace('\n\n', '\n')
                                k4 = k2[i] + '\n' + k3[i]
                                write_msg(event.user_id, k4)
                        if n == 0:
                            write_msg(event.user_id, "Сожалею, в этот день в театре нет никаких спектаклей. Вечер в пустую")
            elif request[:len(request)-11] == 'Малый театр':
                today = requests.get('http://www.xn--80aajbde2dgyi4m.xn--p1ai/')
                today = BeautifulSoup(today.text, "html.parser")
                today = today.find("p", id = "digital_date")
                today = today.getText()
                if int(request[-4:]) > int(today[-4:]) and (int(request[-7:-5]) > int(today[3:5]) or int(request[-7:-5]) == int(today[3:5]) and int(request[-10:-8]) >= int(today[:2])):
                    write_msg(event.user_id, "Прошу прощения, я не вижу так далеко. Как говорится, близорукость не порок")
                elif int(request[-4:]) < int(today[-4:]) or int(request[-4:]) == int(today[-4:]) and int(request[-7:-5]) < int(today[3:5]) or int(request[-4:]) == int(today[-4:]) and int(request[-7:-5]) == int(today[3:5]) and int(request[-10:-8]) < int(today[:2]):
                    write_msg(event.user_id, "Я помню это чудное мгновенье. Но прошлого не вернёшь. Может, посмотришь что-нибудь на будущее?")
                else:
                    date = str(int(request[-10:-8]))
                    t = 0
                    if request[-4:] == '2019':
                        theatre = requests.get('http://www.maly.ru/afisha')
                    elif request[-7:-5] == '01' and int(request[-10:-8]) <= 31:
                        date += ' января'
                        theatre = requests.get('https://www.maly.ru/afisha?month=1&year=2020')
                    elif request[-7:-5] == '02' and (int(request[-10:-8]) <= 28 and int(request[-4:]) % 4 != 0 or int(request[-10:-8]) <= 29 and int(request[-4:]) % 4 == 0):
                        date += ' февраля'
                        theatre = requests.get('https://www.maly.ru/afisha?month=2&year=2020')
                    elif request[-7:-5] == '03' and int(request[-10:-8]) <= 31:
                        date += ' марта'
                        theatre = requests.get('https://www.maly.ru/afisha?month=3&year=2020')
                    elif request[-7:-5] == '04' and int(request[-10:-8]) <= 30:
                        date += ' апреля'
                        theatre = requests.get('https://www.maly.ru/afisha?month=4&year=2020')
                    elif request[-7:-5] == '05' and int(request[-10:-8]) <= 31:
                        date += ' мая'
                        theatre = requests.get('https://www.maly.ru/afisha?month=5&year=2020')
                    elif request[-7:-5] == '06' and int(request[-10:-8]) <= 30:
                        date += ' июня'
                        theatre = requests.get('https://www.maly.ru/afisha?month=6&year=2020')
                    elif request[-7:-5] == '07' and int(request[-10:-8]) <= 31:
                        date += ' июля'
                        theatre = requests.get('https://www.maly.ru/afisha?month=7&year=2020')
                    elif request[-7:-5] == '08' and int(request[-10:-8]) <= 31:
                        date += ' августа'
                        theatre = requests.get('https://www.maly.ru/afisha?month=8&year=2020')
                    elif request[-7:-5] == '09' and int(request[-10:-8]) <= 30:
                        date += ' сентября'
                        theatre = requests.get('https://www.maly.ru/afisha?month=9&year=2020')
                    elif request[-7:-5] == '10' and int(request[-10:-8]) <= 31:
                        date += ' октября'
                        theatre = requests.get('https://www.maly.ru/afisha?month=10&year=2020')
                    elif request[-7:-5] == '11' and int(request[-10:-8]) <= 30:
                        date += ' ноября'
                        theatre = requests.get('https://www.maly.ru/afisha?month=11&year=2020')
                    elif request[-7:-5] == '12' and int(request[-10:-8]) <= 31:
                        date += ' декабря'
                        theatre = requests.get('https://www.maly.ru/afisha?month=12&year=2020')
                    else:
                        t = 1
                    if t == 1:
                        write_msg(event.user_id, "То ли ты не то написал, то ли я не так поняла. Может, попробуем ещё раз?")
                    else:
                        k = BeautifulSoup(theatre.text, "html.parser")
                        k0 = k.select("div.poster-tables__item")
                        n = 0
                        for i in range(len(k0)):
                            k1 = k0[i].find("div", {"class": "dayname"})
                            k1 = k1.getText()
                            if k1 == date:
                                k2 = k0[i].find_all("a", {"class": "l_title"})
                                k4 = k0[i].find_all("div", {"class": "poster-details__time"})
                                n = 1
                        if n == 1:
                            for i in range(len(k2)):
                                k2[i] = k2[i].getText()
                            for i in range(len(k4)):
                                k4[i] = k4[i].getText()
                                k4[i] = k4[i].replace('\t', '')
                            k3 = []
                            for i in range(len(k4)):
                                if k4[i][-1].isdigit() == True:
                                    k3.append(k4[i])
                            for i in range(len(k2)):
                                m = k2[i] + k3[i]
                                write_msg(event.user_id, m)
                        else:
                            write_msg(event.user_id, "Сожалею, в этот день в театре нет никаких спектаклей. Вечер в пустую")
            else:
                write_msg(event.user_id, "Я сегодня не выспалась, повтори ещё разок")
