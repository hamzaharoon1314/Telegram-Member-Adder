from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, PeerUser
from telethon.errors.rpcerrorlist import FloodWaitError, PeerFloodError, UserPrivacyRestrictedError, ChatWriteForbiddenError, UserAlreadyParticipantError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.channels import GetFullChannelRequest, JoinChannelRequest
from telethon import types, utils, errors
import configparser
import sys
import csv
from csv import reader
import traceback
import time
import random
from message import message
import subprocess
import requests
import time
import os
hwid = subprocess.check_output(
    'wmic csproduct get uuid').decode().split('\n')[1].strip()
r = requests.get('https://pastebin.com/GCj809pN')


deltamessage = message
with open('memory.csv', 'r') as deltahash:
    csv_reader = reader(deltahash)
    list_of_rows = list(csv_reader)
    row_number = 1
    col_number = 1
    numdel = list_of_rows[row_number - 1][col_number - 1]

delta = int(numdel)
global nextdelta
nextdelta = delta+1


with open('phone.csv', 'r') as delta_obj:
    csv_reader = reader(delta_obj)
    list_of_rows = list(csv_reader)
    row_number = delta
    col_number = 1
    value = list_of_rows[row_number - 1][col_number - 1]

with open('api.csv', 'r') as delta_obj_id:
    csv_reader = reader(delta_obj_id)
    list_of_rows = list(csv_reader)
    row_number = delta
    col_number = 1
    deltaop = list_of_rows[row_number - 1][col_number - 1]

with open('api.csv', 'r') as hash_obj:
    csv_reader = reader(hash_obj)
    list_of_rows = list(csv_reader)
    row_number = delta
    col_number = 2
    deltaxd = list_of_rows[row_number - 1][col_number - 1]

api_id = int(deltaop)
api_hash = str(deltaxd)
pphone = value


def autos():

    phone = utils.parse_phone(pphone)

    client = TelegramClient(f"sessions/{phone}", api_id, api_hash)

    client.connect()
    if not client.is_user_authorized():
        print('some thing has changed')
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))

    input_file = 'data.csv'
    users = []
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['srno'] = row[0]
            user['username'] = row[1]
            user['id'] = int(row[2])
        #user['access_hash'] = int(row[2])
            user['name'] = row[3]
            users.append(user)

    with open('memory.csv', 'r') as hash_obj:
        csv_reader = reader(hash_obj)
        list_of_rows = list(csv_reader)
        row_number = 1
        col_number = 2
        numnext = list_of_rows[row_number - 1][col_number - 1]

    startfrom = int(numnext)
    nextstart = startfrom+50

    with open('memory.csv', 'r') as hash_obj:
        csv_reader = reader(hash_obj)
        list_of_rows = list(csv_reader)
        row_number = 1
        col_number = 3
        numend = list_of_rows[row_number - 1][col_number - 1]

    endto = int(numend)
    nextend = endto+50

    # Enter your file name.
    with open("memory.csv", "w", encoding='UTF-8') as df:
        writer = csv.writer(df, delimiter=",", lineterminator="\n")
        writer.writerow([nextdelta, nextstart, nextend])
    print("Next")
    j = 0
    for user in users:

        if (int(startfrom) <= int(user['srno'])) and (int(user['srno']) <= int(endto)):
            try:
                j += 1
                status = 'delta'
                receiver = client.get_input_entity(user['username'])
                if user['username'] == "":
                    print("no username, moving to next")
                    continue

                client.send_message(receiver, str(deltamessage))
                status = 'DONE'

                #print("Waiting for 60-180 Seconds...")
                time.sleep(random.randrange(1, 3))

            except UserPrivacyRestrictedError:
                status = 'PrivacyRestrictedError'

            except UserAlreadyParticipantError:
                status = 'ALREADY'

            except PeerFloodError as g:
                status = 'PeerFloodError :('
            except FloodWaitError as t:
                stime = t.seconds
                print(f"wait {stime} seconds")
                time.sleep(stime)
            except errors.RPCError as e:
                status = e.__class__.__name__

            except:
                traceback.print_exc()
                print("Unexpected Error")
                continue
            print(f"SENDING TO {user['name']} TOTAL: {j} - {status}")
        elif int(user['srno']) > int(endto):
            print("Message sended Successfully!")
            stat = input(
                'Done!\nChoose From Below:\n\n1 - Repeat The Script\nOR Just Hit Enter To Quit\n\nEnter: ')
            if stat == '1':
                autos()
            else:
                quit()


autos()
