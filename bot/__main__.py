from pyrogram import filters
from pyrogram import idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from bot import bot, data, Config, LOGS, list_handler, LOG_FILE_NAME, col, td
import asyncio, traceback, time, pyrogram
from datetime import datetime
from bot.plugins.upload import upload
from bot.plugins.authorise import authorise, teamdrive_auth
from bot.plugins.utils import add_task, on_task_complete
from bot.plugins.html import html, html2

START_TIME = datetime.now()

@bot.on_message(filters.incoming & (filters.video | filters.document))
async def help_message(bot, message):
  if message.chat.id not in Config.AUTH_USERS:
   return
  data.append(message)
  if len(data) == 1:
   await add_task(data[0])

@bot.on_message(filters.incoming & filters.command(["uptime"]))
async def help_message(bot, message):
  try:
   if message.from_user.id in Config.AUTH_USERS:
    await bot.send_message(chat_id=message.from_user.id,text=f"**Uptime**: {str(datetime.now() - START_TIME).split('.')[0]}**")
    return
   else:
    return await message.reply_sticker("CAACAgUAAxkBAAIah2LNhR_vCtyL-YCw8Sf3cO0BCFnqAAKDBgACmStpV778w4PJK2OkHgQ")
  except Execption as e:
    print(e)

@bot.on_message(filters.incoming & filters.command(["start"]))
async def help_message(bot, message):
  if message.chat.id not in Config.AUTH_USERS:
    return
  txt = "**Simple Gdrive Bot**"
  await bot.send_message(chat_id=message.chat.id,text=txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Join Fiercenetwork', url='https://t.me/Fiercenetwork')]]), reply_to_message_id=message.id)

@bot.on_message(filters.incoming & filters.command(["authorise"]))
async def help_message(bot, message):
  if message.chat.id not in Config.AUTH_USERS:
    return
  await authorise(bot, message)

@bot.on_message(filters.incoming & filters.command(["upload"]))
async def help_message(bot, message):
  if message.chat.id not in Config.AUTH_USERS:
    return
  if message.reply_to_message:
   bc = await message.reply_text("Downloading The Video")
   filename = await bot.download_media(message.reply_to_message)
   await bc.edit("Trying To Upload")
   bcc = upload(filename, message)
   print(bcc)
   if not bcc == 'Not_Authorised':
     await bc.edit(bcc)
   else:
     await bc.edit("Not Authorised")


@bot.on_message(filters.incoming & filters.command(["html2"]))
async def help_message(bot, message):
  if message.chat.id not in Config.AUTH_USERS:
    return
  await html2(bot, message)

@bot.on_message(filters.incoming & filters.command(["logs"]))
async def help_message(bot, message):
  if message.from_user.id in Config.AUTH_USERS:
      await bot.send_document(chat_id=message.from_user.id, document=LOG_FILE_NAME, reply_to_message_id=message.id)

@bot.on_message(filters.incoming & filters.command(["clear"]))
async def help_message(bot, message):
 if message.from_user.id in Config.AUTH_USERS:
  data.clear()

@bot.on_message(filters.incoming & filters.command(["revoke"]))
async def help_message(bot, message):
 if message.from_user.id in Config.AUTH_USERS:
    if col.find_one({'id' : message.from_user.id}):
        virgin = col.find_one({'id' : message.from_user.id})
        col.delete_one(virgin)
        await bot.send_message(chat_id=message.from_user.id , text="Revoked Your Account", reply_to_message_id=message.id)
    else:
        await bot.send_message(chat_id=message.from_user.id , text="Authorise Your Account First", reply_to_message_id=message.id)

@bot.on_message(filters.incoming & filters.command(["tdvoke"]))
async def help_message(bot, message):
 if message.from_user.id in Config.AUTH_USERS:
    if td.find_one({'id' : message.from_user.id}):
        virgin = td.find_one({'id' : message.from_user.id})
        td.delete_one(virgin)
        await bot.send_message(chat_id=message.from_user.id , text="Revoked Your TD", reply_to_message_id=message.id)
    else:
        await bot.send_message(chat_id=message.from_user.id , text="Authorise Your TD First Using /td", reply_to_message_id=message.id)

@bot.on_message(filters.incoming & filters.command(["td"]))
async def help_message(bot, message):
 if message.from_user.id in Config.AUTH_USERS:
    await teamdrive_auth(bot, message)



bot.run()
