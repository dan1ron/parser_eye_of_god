from bs4 import BeautifulSoup as bs
from pyrogram.errors import BadRequest
import os
    
output = {}

async def message_parser(message, app):
    if len(message.reply_markup.inline_keyboard) > 1:
        txt = message.text
        number = txt.partition('Номер: ')[2].partition('\n')[0]
        country = txt.partition('Страна: ')[2].partition('\n')[0]
        region = txt.partition('Регион: ')[2].partition('\n')[0]
        operator = txt.partition('Оператор: ')[2].partition('\n')[0]

        possible_names = txt.partition('Возможные имена:\n└ ')[2].partition('\n\n')[0]
        full_name = txt.partition('ФИО:\n')[2].partition('\n')[0]
        possible_addres = txt.partition('Возможные адреса: \n')[2].partition('\n\n')[0]
        date_of_birth = txt.partition('Дата рождения: ')[2].partition('\n')[0]
        email = txt.partition('Email: ')[2].partition('\n')[0]
        telegram = txt.partition('Telegram: ')[2].partition('\n')[0]

        # pars links
        link : list = message.entities
        links = {
            'VK':None, 
            'Facebook':None, 
            'OK':None, 
            'Telegram':[]
        }
        for l in link:
            if l.url:
                if l.url.find('https://vk.com') != -1:
                    links['VK'] = l.url
                elif l.url.find('https://www.facebook.com') != -1:
                    links['Facebook'] = l.url
                elif l.url.find('https://ok.ru') != -1:
                    links['OK'] = l.url
                else:
                    links['Telegram'].append(l.url)
        global output
        output = {
            "number": number,
            "country": country, 
            "region": region,
            "operator": operator,
            "possible_names": possible_names,
            "full_name": full_name,
            "possible_addres": possible_addres,
            "date_of_birth": date_of_birth,
            "email": email,
            "telegram": telegram,
            "links": links,
            "ads": []
        }
        try:    #click button
            await app.request_callback_answer(chat_id=message.chat.id, message_id=message.id, callback_data= f"FREE|ads|{number}")
        except BadRequest:
            html_parser()                



def html_parser(html=None):
    if html != None: 
        try:
            with open(f"data_html/{html}", encoding='utf-8', mode='r') as file:
                src = file.read()
        except Exception:
            pass

        soup = bs(src, "lxml")
        cards = soup.find_all("div", class_="prod_search_ui")

        for card in cards:
            title = card.find('a', class_= 'title_ads').text
            link = card.find('a', class_= 'title_ads').get("href")
            data_class_location_ads = card.find_all('div', class_="location_ads")
            tag = data_class_location_ads[0].text
            description = data_class_location_ads[1].text
            location = data_class_location_ads[2].text
            time = card.find('div', class_="ads_time").text

            ads = {
                "title": title,
                "link": link,
                "tag": tag,
                "description": description,
                "location": location,
                "time": time
            }

            output['ads'].append(ads)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f"data_html/{html}")
        os.remove(path)
    else:
        output['ads']='not found'
        
    print(output) #выходные данные