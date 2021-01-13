import csv
import configparser
import traceback

from telethon.sync import TelegramClient
from telethon import types, utils, errors
from telethon.tl.functions import channels
from add import read_csv, write_csv


try:
    config = configparser.ConfigParser()
    config.read("config.ini")

    channel = config['Telegram']['from_channel']
    phone = utils.parse_phone(config['Telegram']['main_phone'])
    api = read_csv('api.csv')[0]


    client = TelegramClient(f"sessions/{phone}", *api)
    client.start(phone)


    rows = [
        ['ID', 'Name', 'Username', 'Phone']
    ]

    print("Getting participants...")

    for participant in client.iter_participants(channel, aggressive=True):
        print(f"Got {len(rows)}", end='\r')
        rows.append([
            participant.id,
            utils.get_display_name(participant),
            participant.username,
            participant.phone
        ])


    print("\nWriting output")
    write_csv('users.csv', rows)
    print("Done!")


finally:
    input()