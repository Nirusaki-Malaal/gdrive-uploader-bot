from pydrive.auth import GoogleAuth, AuthenticationError
from bot import col, bot, Config, LOGS, td
import json, pyrogram, time, datetime, asyncio, os
from pydrive.drive import GoogleDrive
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

async def if_user(message):
   if col.find_one({'id' : message.from_user.id}):
      return True
   else:
      return False

async def teamdrive_auth(bot, message):
    if not col.find_one({'id' : message.from_user.id}):
        return await bot.send_message(chat_id= message.from_user.id , text="Better Authorise First", reply_to_message_id = message.id)
    if td.find_one({'id' : message.from_user.id}):
        return await bot.send_message(chat_id= message.from_user.id , text="TD Is Already Registered Use /tdvoke To Revoke TD", reply_to_message_id = message.id)
    else:
        td_id = await bot.ask(chat_id=message.from_user.id, text="Enter TEAMDRIVE_ID\nNote :\nAny Detail Being Wrong Will Break Upload Sequence", reply_to_message_id=message.id)
        teamDriveId = td_id.text
        td_folder_id = await bot.ask(chat_id=message.from_user.id, text="Enter TEAMDRIVE_FOLDER_ID\nNote :\nAny Detail Being Wrong Will Break Upload Sequence", reply_to_message_id=td_id.id)
        td.insert_one({'id' : message.from_user.id, 'TEAMDRIVE_ID' : teamDriveId, 'TEAMDRIVE_FOLDER_ID' : str(td_folder_id.text)})
        await bot.send_message(chat_id= message.from_user.id , text="Succesfully Registered Your Teamdrive", reply_to_message_id = td_folder_id.id)


async def authorise(bot, message):
    gauth = GoogleAuth()
    if col.find_one({'id' : message.from_user.id}):
     dictionary = col.find_one({'id' : message.from_user.id})
     credentials = str(dictionary['credentials']) ## credentials
     if not os.path.exists(str(message.from_user.id)):
      with open(f'{str(message.from_user.id)}' , 'w') as file1:
       p = file1.write(credentials)
       file1.close()
     gauth.LoadCredentialsFile(str(message.from_user.id))
     if gauth.access_token_expired:
        gauth.Refresh() ## Refresh Token If Expired ##
        await bot.send_message(chat_id=message.from_user.id, text="Refreshed Authorisation")
     else:
        gauth.Authorize() ## Authorising With Saved Credentials ##
        await bot.send_message(chat_id=message.from_user.id, text="Already Authorised")
    else:
     authurl = gauth.GetAuthUrl()
     input1 = await bot.ask(chat_id=message.from_user.id, reply_to_message_id=message.id, text="Open This Url And Send The Authorisation Code" ,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Link', url=authurl)]])) ## Listening
     try:
      drive = gauth.Auth(str(input1.text))
      gauth.SaveCredentialsFile(str(message.from_user.id))
      with open(str(message.from_user.id) , 'r') as file2:
       b = file2.read()
       file2.close()
      col.insert_one({'id': message.from_user.id, 'credentials' : b})
      await bot.send_message(chat_id=message.from_user.id, text="Authorized")
     except AuthenticationError as e:
      await bot.send_message(message.from_user.id, "Wrong Token Entered")

async def revoke(bot, message):
   if col.find_one({'id' : message.from_user.id}):
      col.delete_one({'id' : message.from_user.id})
      await bot.send_message(text="Revoked", chat_id=message.from_user.id, reply_to_message_id=message.id)
   else:
      await bot.send_message(text="Authorise First Do /authorise To Authorise", chat_id=message.from_user.id, reply_to_message_id=message.id)

def check_user(message):
   gauth = GoogleAuth()
   if col.find_one({'id' : message.from_user.id}):
     dictionary = col.find_one({'id' : message.from_user.id})
     credentials = str(dictionary['credentials']) ## Credentials ##
     if not os.path.exists(str(message.from_user.id)):
      with open(f'{str(message.from_user.id)}' , 'w') as file1:
       p = file1.write(credentials)
       file1.close()
     gauth.LoadCredentialsFile(str(message.from_user.id))
     if gauth.access_token_expired:
        gauth.Refresh() ## Refresh Token If Expired ##
     else:
        gauth.Authorize() ## Authorising With Saved Credentials ##

async def proceed_or_not(message):
    if col.find_one({'id' : message.from_user.id}):
        return "proceed"
    else:
       await bot.send_message(message.from_user.id , "Authorise First Newbie Use /authorise")
       return "quit"
    if td.find_one({'id' : message.from_user.id}):
      return "proceed"
    else:
       await bot.send_message(message.from_user.id , "Teamdrive Not Registered Use /td To Authorise Team Drive")
       return "quit"
