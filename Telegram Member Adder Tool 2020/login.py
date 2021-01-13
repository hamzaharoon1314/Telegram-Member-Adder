from telethon.sync import TelegramClient
from telethon import utils
from add import read_csv


done = False
try:
    phone_list = sum(read_csv('phone.csv'), start=[])
    api = read_csv('api.csv')[0]


    for unparsed_phone in phone_list:
        phone = utils.parse_phone(unparsed_phone)
        
        print(f"Login {phone}")
        client = TelegramClient(f"sessions/{phone}", *api)
        client.start(phone)

        client.disconnect()
        print()

    done = True


finally:
    input("Done!" if done else "Error!")