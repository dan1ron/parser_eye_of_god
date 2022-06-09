from pyrogram import Client, filters
import pars

api_id= 00000000
api_hash = ''

# Welcome message template
app = Client("bot")
print('client launch')

my = 00000000

TARGET = 1827122521
# Filter in only new_chat_members updates generated in TARGET chat

@app.on_message(filters.text)
async def text(client, message):
    if message.from_user.id == TARGET:
        await pars.message_parser(message, app)
    elif message.from_user.id == my:
        await app.send_message(TARGET, message.text)

@app.on_message(filters.chat(TARGET)&filters.media)
async def file(client, message):
    await app.download_media(message.document.file_id, file_name=f'data_html/{message.document.file_name}')
    pars.html_parser(message.document.file_name)


if __name__ == "__main__":
    app.run()
    