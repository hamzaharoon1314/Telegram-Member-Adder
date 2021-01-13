from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest, GetFullChannelRequest
from telethon import types, utils, errors
import sys
import csv
import traceback
import time
import random
import os
import re

ve = int(input("Which Account You Want To Use?\n\nEnter: "))
with open('../phone.csv', 'r') as read_obj:
    csv_reader = csv.reader(read_obj)
    list_of_rows = list(csv_reader)   
    row_number = ve
    col_number = 1
    value = list_of_rows[row_number - 1][col_number - 1]
    
with open('../api.csv', 'r') as api_obj_id:
    csv_reader = csv.reader(api_obj_id)
    list_of_rows = list(csv_reader)    
    row_number = ve
    col_number = 1
    deltaop = list_of_rows[row_number - 1][col_number - 1]
    
with open('../api.csv', 'r') as hash_obj:
    csv_reader = csv.reader(hash_obj)
    list_of_rows = list(csv_reader)
    row_number = ve
    col_number = 2
    deltaxd = list_of_rows[row_number - 1][col_number - 1]
    
api_id = int(deltaop)
api_hash = str(deltaxd)
pphone = value
phone = utils.parse_phone(pphone)
print(f"Using {phone} - Along With {api_id}")
client = TelegramClient(f"../sessions/{phone}", api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

def add_users_to_group():
    global ve
    input_file = f'data/data{ve}.csv'
    users = []
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['srno'] = row[0]
            user['username'] = row[1]
            try:
                user['id'] = int(row[2])
                user['access_hash'] = int(row[3])
                user['name'] = row[4]
            except IndexError:
                print ('users without id or access_hash')
            users.append(user)
    #random.shuffle(users)
    chats = []
    last_date = None
    chunk_size = 10
    groups=[]

    result = client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash = 0
            ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup== True: # CONDITION TO ONLY LIST MEGA GROUPS.
                groups.append(chat)
                
        except:
            continue

    print('Choose a group to add members:')
    i=0
    for group in groups:
        print(str(i) + '- ' + group.title)
        i+=1

    g_index = input("Enter a Number: ")
    target_group=groups[int(g_index)]
    print('\n\nGroup Selected:\t' + groups[int(g_index)].title)

    target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)

    mode = int(input("Enter 1 to add by username or 2 to add by ID: "))
    startfrom = int(input("Start From = "))
    endto = int(input("End To = "))
    delta_xd = False
    error_count = 0

    for user in users:
        global status
        
        status = 'do'
        countt = 6
        if (int(startfrom) <= int(user['srno'])) and (int(user['srno']) <= int(endto)):

            try:
     
                if mode == 1:
                    if user['username'] == "":
                        print('no username, moving to next')
                        continue
                    user_to_add = client.get_input_entity(user['username'])
                elif mode == 2:
                    user_to_add = InputPeerUser(user['id'], user['access_hash'])
                else:
                    sys.exit("Invalid Mode Selected. Please Try Again.")
                client(InviteToChannelRequest(target_group_entity,[user_to_add]))
                #print("Waiting 60 Seconds...")
                status = 'DONE'
                time.sleep(5)
            except PeerFloodError:
                status = 'PeerFloodError'
                print('Script Is Stopping Now For 24 Hours')
                time.sleep(86400)
                #print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
            except UserPrivacyRestrictedError:
                status = 'PrivacyError'
                #print("The user's privacy settings do not allow you to do this. Skipping.")
            except errors.RPCError as e:
                status = e.__class__.__name__
        
    
            except Exception as d:
            	status = d
            except:
                traceback.print_exc()
                print("Unexpected Error")
                error_count += 1
                if error_count > 10:
                    sys.exit('too many errors')
                continue
            channel_full_info = client(GetFullChannelRequest(channel=target_group_entity))
                
            countt = int(channel_full_info.full_chat.participants_count)

            print(f"ADDING {user['name']} TO {target_group.title} TOTAL: {countt} - {status}")
        elif int(user['srno']) > int(endto):
            #print("Members Added Successfully!")
            delta_xd = True
    print("Done!" if delta_xd else "Error!")       

def list_users_in_group():
    global ve
    chats = []
    last_date = None
    chunk_size = 200
    groups=[]
    
    result = client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash = 0
            ))
    chats.extend(result.chats)
    
    for chat in chats:
        try:
            if chat.megagroup== True:
                groups.append(chat)
            # if chat.megagroup== True:
        except:
            continue
    
    print('Choose a group to scrape members from:')
    i=0
    for g in groups:
        print(str(i) + '- ' + g.title)
        i+=1
    
    g_index = input("Enter a Number: ")
    target_group=groups[int(g_index)]

    print('\n\nGroup Selected:\t' + groups[int(g_index)].title)
    
    print('Fetching Members...')
    all_participants = []
    all_participants = client.get_participants(target_group, aggressive=True)
    
    print('Saving In file...')
    
    with open(f"data/data{ve}.csv","w",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['sr. no.','username','user id', 'access hash','name','group', 'group id', 'status'])
        i = 0
        for user in all_participants:
            i += 1
            if user.username:
                username= user.username
            else:
                username= ""
            if user.first_name:
                first_name= user.first_name
            else:
                first_name= ""
            if user.last_name:
                last_name= user.last_name
            else:
                last_name= ""
            name= (first_name + ' ' + last_name).strip()
            if isinstance(user.status, types.UserStatusOnline):
                status = 1
        
            elif isinstance(user.status, types.UserStatusOffline):
                if time.time()-(user.status.was_online).timestamp() <=86400:
                    status = 2
                else:
                    status = 31634268763763
            writer.writerow([i,username,user.id,user.access_hash,name,target_group.title, target_group.id, status])      
    print('Members scraped successfully.')
    

def printCSV():
    global ve
    


    lines = list()


    def main():
        lines = list()
        with open(f'data/data{ve}.csv', 'r',encoding='UTF-8') as readFile:

            reader = csv.reader(readFile)

            for row in reader:

                lines.append(row)

                for field in row:

                    if field == '31634268763763':
                        lines.remove(row)
        with open('11.csv', 'w', encoding='UTF-8') as writeFile:
            writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")

            writer.writerows(lines)

    def main1():
        lines = list()
        with open('11.csv', 'r',encoding='UTF-8') as readFile:

            reader = csv.reader(readFile)

            for row in reader:

                lines.append(row)

                for field in row:

                    if field == 'username':
                        lines.remove(row)
        
        with open('22.csv', 'w', encoding='UTF-8') as writeFile:
            writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")

            writer.writerows(lines)

    main()
    main1()


    with open("22.csv","r",encoding='UTF-8') as source:
        rdr = csv.reader(source)

        with open(f"data/data{ve}.csv","w",encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['sr. no.','username','user id', 'access hash','name','group', 'group id', 'status'])
            i = 0
            for row in rdr:
                i += 1
                writer.writerow((i,row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                
                
    os.remove("11.csv")
    os.remove("22.csv")
    #os.remove("unf.csv")
    print(f"Successfully Filtered And Saved In data{ve}.csv")
    
    

# print('Fetching Members...')
# all_participants = []
# all_participants = client.get_participants(target_group, aggressive=True)
def autos():
    print('What do you want to do:')
    mode = int(input("Enter \n1-Scrape users from a group\n2-Add users from CSV to Group\n3-Filter By Last Seen\n4-Scrape Members To csv file Then Add Them To Group\n5-Scrape Members And Filter Them\n6-Filter data Then Add Them To Group\n7-Scrape Members, Then Filter, Then Add To Group\n\nYour option:  "))


    if mode == 1:
        list_users_in_group()
    elif mode == 2:
        add_users_to_group()
    elif mode == 3:
        printCSV()
    elif mode == 4:
        list_users_in_group()
        add_users_to_group()
    elif mode == 5:
        list_users_in_group()
        printCSV()
    elif mode == 6:
        printCSV()
        add_users_to_group()
    elif mode == 7:
        list_users_in_group()
        printCSV()
        add_users_to_group()
autos()
stat = input('Done!\nChoose From Below:\n\n1 - Repeat The Script\nOR Just Hit Enter To Quit\n\nEnter: ')
if stat == '1':
    autos()

else:
    quit()
    
