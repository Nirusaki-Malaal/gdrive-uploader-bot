import os

from pydrive.auth import AuthenticationError, GoogleAuth
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import bot, col, td


async def teamdrive_auth(bot, message):
    user_id = message.from_user.id
    if not col.find_one({"id": user_id}):
        return await bot.send_message(
            chat_id=user_id,
            text="Better Authorise First",
            reply_to_message_id=message.id,
        )

    if td.find_one({"id": user_id}):
        return await bot.send_message(
            chat_id=user_id,
            text="TD is already registered. Use /tdvoke to revoke TD",
            reply_to_message_id=message.id,
        )

    td_id = await bot.ask(
        chat_id=user_id,
        text="Enter TEAMDRIVE_ID\nNote:\nAny wrong detail will break upload sequence",
        reply_to_message_id=message.id,
    )
    td_folder_id = await bot.ask(
        chat_id=user_id,
        text="Enter TEAMDRIVE_FOLDER_ID\nNote:\nAny wrong detail will break upload sequence",
        reply_to_message_id=td_id.id,
    )
    td.insert_one(
        {
            "id": user_id,
            "TEAMDRIVE_ID": td_id.text,
            "TEAMDRIVE_FOLDER_ID": td_folder_id.text,
        }
    )
    await bot.send_message(
        chat_id=user_id,
        text="Successfully registered your Team Drive",
        reply_to_message_id=td_folder_id.id,
    )


async def authorise(bot, message):
    user_id = message.from_user.id
    gauth = GoogleAuth()

    existing = col.find_one({"id": user_id})
    if existing:
        credentials = str(existing["credentials"])
        if not os.path.exists(str(user_id)):
            with open(str(user_id), "w", encoding="utf-8") as file_obj:
                file_obj.write(credentials)

        gauth.LoadCredentialsFile(str(user_id))
        if gauth.access_token_expired:
            gauth.Refresh()
            await bot.send_message(chat_id=user_id, text="Refreshed Authorisation")
        else:
            gauth.Authorize()
            await bot.send_message(chat_id=user_id, text="Already Authorised")
        return

    authurl = gauth.GetAuthUrl()
    input1 = await bot.ask(
        chat_id=user_id,
        reply_to_message_id=message.id,
        text="Open this URL and send the authorisation code",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Link", url=authurl)]]),
    )

    try:
        gauth.Auth(str(input1.text))
        gauth.SaveCredentialsFile(str(user_id))
        with open(str(user_id), "r", encoding="utf-8") as file_obj:
            credentials = file_obj.read()
        col.insert_one({"id": user_id, "credentials": credentials})
        await bot.send_message(chat_id=user_id, text="Authorized")
    except AuthenticationError:
        await bot.send_message(user_id, "Wrong token entered")


def check_user(message):
    user_id = message.from_user.id
    if not col.find_one({"id": user_id}):
        return

    gauth = GoogleAuth()
    credentials = str(col.find_one({"id": user_id})["credentials"])
    if not os.path.exists(str(user_id)):
        with open(str(user_id), "w", encoding="utf-8") as file_obj:
            file_obj.write(credentials)

    gauth.LoadCredentialsFile(str(user_id))
    if gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()


async def proceed_or_not(message):
    user_id = message.from_user.id
    if not col.find_one({"id": user_id}):
        await bot.send_message(user_id, "Authorise first. Use /authorise")
        return "quit"

    if not td.find_one({"id": user_id}):
        await bot.send_message(user_id, "Team Drive not registered. Use /td")
        return "quit"

    return "proceed"
