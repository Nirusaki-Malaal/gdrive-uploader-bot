from datetime import datetime

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import Config, LOG_FILE_NAME, bot, col, data, td
from bot.plugins.authorise import authorise, teamdrive_auth
from bot.plugins.html import html2
from bot.plugins.upload import upload
from bot.plugins.utils import add_task

START_TIME = datetime.now()


def is_authorized(message) -> bool:
    return message.from_user and message.from_user.id in Config.AUTH_USERS


@bot.on_message(filters.incoming & (filters.video | filters.document))
async def queue_upload(_, message):
    if not is_authorized(message):
        return
    data.append(message)
    if len(data) == 1:
        await add_task(data[0])


@bot.on_message(filters.incoming & filters.command(["uptime"]))
async def uptime_handler(_, message):
    try:
        if not is_authorized(message):
            return await message.reply_sticker(
                "CAACAgUAAxkBAAIah2LNhR_vCtyL-YCw8Sf3cO0BCFnqAAKDBgACmStpV778w4PJK2OkHgQ"
            )
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"**Uptime**: {str(datetime.now() - START_TIME).split('.')[0]}",
        )
    except Exception as exc:
        print(exc)


@bot.on_message(filters.incoming & filters.command(["start"]))
async def start_handler(_, message):
    if not is_authorized(message):
        return
    await bot.send_message(
        chat_id=message.chat.id,
        text="**Simple Gdrive Bot**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Join Fiercenetwork", url="https://t.me/Fiercenetwork")]]
        ),
        reply_to_message_id=message.id,
    )


@bot.on_message(filters.incoming & filters.command(["authorise"]))
async def authorise_handler(_, message):
    if is_authorized(message):
        await authorise(bot, message)


@bot.on_message(filters.incoming & filters.command(["upload"]))
async def upload_handler(_, message):
    if not is_authorized(message) or not message.reply_to_message:
        return

    status = await message.reply_text("Downloading The File")
    filename = await bot.download_media(message.reply_to_message)
    await status.edit("Trying To Upload")

    result = await upload(filename, message)
    if result and result != "Not_Authorised":
        await status.edit(result)
    else:
        await status.edit("Not Authorised")


@bot.on_message(filters.incoming & filters.command(["html2"]))
async def html2_handler(_, message):
    if is_authorized(message):
        await html2(bot, message)


@bot.on_message(filters.incoming & filters.command(["logs"]))
async def logs_handler(_, message):
    if is_authorized(message):
        await bot.send_document(
            chat_id=message.from_user.id,
            document=LOG_FILE_NAME,
            reply_to_message_id=message.id,
        )


@bot.on_message(filters.incoming & filters.command(["clear"]))
async def clear_handler(_, message):
    if is_authorized(message):
        data.clear()


@bot.on_message(filters.incoming & filters.command(["revoke"]))
async def revoke_handler(_, message):
    if not is_authorized(message):
        return

    if col.find_one({"id": message.from_user.id}):
        col.delete_one({"id": message.from_user.id})
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Revoked Your Account",
            reply_to_message_id=message.id,
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Authorise Your Account First",
            reply_to_message_id=message.id,
        )


@bot.on_message(filters.incoming & filters.command(["tdvoke"]))
async def tdvoke_handler(_, message):
    if not is_authorized(message):
        return

    if td.find_one({"id": message.from_user.id}):
        td.delete_one({"id": message.from_user.id})
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Revoked Your TD",
            reply_to_message_id=message.id,
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Authorise Your TD First Using /td",
            reply_to_message_id=message.id,
        )


@bot.on_message(filters.incoming & filters.command(["td"]))
async def td_handler(_, message):
    if is_authorized(message):
        await teamdrive_auth(bot, message)


bot.run()
