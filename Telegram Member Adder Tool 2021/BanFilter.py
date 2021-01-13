from telethon.sync import TelegramClient
from telethon import utils
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import csv
import configparser


config = configparser.ConfigParser()
config.read("config.ini")
export_phone = config['Telegram']['export_phone']
export_api_id = config['Telegram']['export_api_id']
export_api_hash = config['Telegram']['export_api_hash']
from_group = config['Telegram']['from_channel']


api_id = int(export_api_id)   
api_hash = str(export_api_hash)
MadeByDeltaXd = []



done = False
with open('phone.csv', 'r') as f:
    str_list = [row[0] for row in csv.reader(f)]


    po = 0
    for unparsed_phone in str_list:
        po += 1
        
       
        phone = utils.parse_phone(unparsed_phone)
        
        print(f"Login {phone}")
        client = TelegramClient(f"sessions/{phone}", api_id, api_hash)
        #client.start(phone)
        client.connect()
        if not client.is_user_authorized():
            try:
                print('This Phone Has Been Revoked')
                delta_xd = str(po)
                delta_op = str(unparsed_phone)
                MadeByDeltaXd.append(delta_xd+' - '+delta_op)
                continue
                
            except PhoneNumberBannedError:
                print('Ban')
                delta_xd = str(po)
                delta_op = str(unparsed_phone)
                MadeByDeltaXd.append(delta_xd+' - '+delta_op)
                

                continue
            
        

        #client.disconnect()
        print()
    done = True
    print('List Of Banned Numbers')
    print(*MadeByDeltaXd,sep='\n')
    print('Saved In BanNumers.csv')
    with open('BanNumbers.csv', 'w', encoding='UTF-8') as writeFile:
        writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")

        writer.writerows(MadeByDeltaXd)
    

input("Done!" if done else "Error!")
