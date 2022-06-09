from pyrogram import Client

id_main_bot = 00000000

api_id = 0000000
api_hash = ''

app = Client("my_account", api_id, api_hash)

def send_phone_number(number):
    with app:
        app.send_message(id_main_bot, number)
    
