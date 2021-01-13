import csv
import configparser
import time
import traceback
from typing import List, Union

from telethon.sync import TelegramClient
from telethon import types, utils, errors
from telethon.tl.functions import channels, contacts



def print_output(
    client: TelegramClient,
    channel: Union[types.Channel, str]=None,
    user: Union[types.User, str]=None,
    status=None
    ):
    """Print output in table row format"""
    client_disp = utils.get_display_name(client.get_me()).ljust(20)
    
    if isinstance(channel, str):
        channel_disp = channel.ljust(20)
    else:
        channel_disp = channel.username.ljust(20) if channel else 'None'.ljust(20)

    if isinstance(user, str):
        user_disp = user
    else:
        user_disp = utils.get_display_name(user).ljust(40) if user else 'None'.ljust(40)

    print(f"{client_disp} | {channel_disp} | {user_disp} | {status.ljust(40)}")



def join_channel(client: TelegramClient, channel) -> bool:
    """Join channel. Returns whether client joined or not."""
    try:
        client(channels.JoinChannelRequest(channel))
        
    except errors.RPCError:
        return False
    
    # Verify if client joined channel or not
    chat = client(channels.GetChannelsRequest(
        [channel]
    )).chats[0]

    return not chat.left and not chat.restricted



def add_user_to_channel(client: TelegramClient, user: types.User, channel) -> bool:
    # Get user entity from channel participants list
    users = list(filter(
        lambda u: u.id == user.id,
        client.get_participants(channel, search=utils.get_display_name(user))
    ))
    
    if users:
        status = "Already"


    else:
        try:
            client(channels.InviteToChannelRequest(
                channel,
                [ user ]
            ))

            status = "Done"

        except errors.FloodWaitError as e:
            status = f"Wait {e.seconds} seconds. Skipped!"

        except errors.RPCError as e:
            status = e.__class__.__name__

        except:
            status = "UnexpectedError"
            traceback.print_exc()


    channel_entity = client.get_entity(channel)
    print_output(client, channel_entity, user, status)

    if status in [
        "Done",
        "Already",
        "UserChannelsTooMuchError",
        "UsersTooMuchError",
        "UserNotMutualContactError",
        "UserPrivacyRestrictedError"
    ]:
        return True
    else:
        return False



def read_csv(input_file):
    file_rows = open(input_file, encoding='UTF-8').readlines()
    file_content = set(map(lambda r: r.strip(), file_rows))
    
    if '' in file_content:
        file_content.remove('')
    file_content.remove(file_rows[0].strip())

    reader = csv.reader(file_content, delimiter=",")

    rows = [ row for row in reader ]
    return rows



def write_csv(output_file, rows) -> List[List[str]]:
    f = open(output_file, 'w+', encoding='utf-8', newline='')
    writer = csv.writer(f, delimiter=',')

    writer.writerows(rows)
    f.close()



if __name__ == '__main__':
    done = False
    try:
        api_info_list = read_csv('api.csv')
        phone_list = sum(read_csv('phone.csv'), start=[])

        config = configparser.ConfigParser()
        config.read("config.ini")
        from_channel = config['Telegram']['from_channel']
        to_channel = config['Telegram']['to_channel']
        main_phone = utils.parse_phone(config['Telegram']['main_phone'])

        user_rows = read_csv('users.csv')


        main_client = TelegramClient(f"sessions/{main_phone}", *api_info_list[0])
        main_client.start(main_phone)

        from_channel_entity = main_client.get_entity(from_channel)
        to_channel_entity = main_client.get_entity(to_channel)
        
        
        try:
            for api in api_info_list:
                print(f"\n*** Using App {api[0]} ***\n")

                for unparsed_phone in phone_list:
                    phone = utils.parse_phone(unparsed_phone)
                    client = TelegramClient(f"sessions/{phone}", *api)
                    client.start(phone)

                    # Join channels
                    channels_joined = all([
                        join_channel(client, from_channel),
                        join_channel(client, to_channel)
                    ])
                    if not channels_joined:
                        print_output(client, status="Cannot join channels")
                        continue


                    me = client.get_me()
                    main_client(contacts.ImportContactsRequest([
                        types.InputPhoneContact(0, phone, me.first_name or '.', me.last_name or '.')
                    ]))

                    if from_channel_entity.broadcast:
                        main_client.edit_admin(from_channel, phone, is_admin=True)
                    if to_channel_entity.broadcast:
                        main_client.edit_admin(to_channel, phone, is_admin=True)


                    while user_rows:
                        row = user_rows.pop(0)
                        user_id = int(row[0])
                        name = row[1]

                        user = list(filter(
                            lambda u: u.id == user_id,
                            client.get_participants(from_channel, search=name)
                        ))
                        if not user:
                            print_output(client, to_channel, status="Could not find user")
                            continue
                        
                        user = user[0]
                        success = add_user_to_channel(client, user, to_channel)

                        if success:
                            time.sleep(0)
                        else:
                            user_rows.insert(0, row)
                            break


                    if from_channel_entity.broadcast:
                        main_client.edit_admin(from_channel, phone, is_admin=False)
                    if to_channel_entity.broadcast:
                        main_client.edit_admin(to_channel, phone, is_admin=False)

                    client.disconnect()

        except KeyboardInterrupt:
            print("\nCancelled!")

        done = True


    finally:
        print("Done!" if done else "Error!")