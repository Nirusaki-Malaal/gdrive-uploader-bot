import math
import os
import time

from pyrogram.types import Message

from bot import bot, data
from .upload import upload


async def progress_for_pyrogram(current, total, bot, ud_type, message, start):
    now = time.time()
    diff = max(now - start, 1e-6)

    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total if total else 0
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000 if speed else 0
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        finished = "▣" * math.floor(percentage / 10)
        unfinished = "□" * (10 - math.floor(percentage / 10))
        progress_bar = f"{finished}{unfinished}"

        messg = (
            f"{ud_type}\n"
            f"➣ **Ꮲᴇrᴄᴇnᴛ** 🗿 : {round(percentage, 2)}\n"
            f"➣ **Ꭲᴏᴛᴀl Ꮪizᴇ** 🎯 : {humanbytes(total)}\n"
            f"➣ **Ꮯᴏʍᴩlᴇᴛᴇd** 🏗 : {humanbytes(current)}\n"
            f"➣ **Ꭲiʍᴇ Ꮮᴇfᴛ** ⌛️ : {estimated_total_time if estimated_total_time else '0 s'}\n"
            f"➣ **Ꮪᴩᴇᴇd** 🚀 : {humanbytes(speed)}\n"
            f"➢ {progress_bar}"
        )

        try:
            if not message.photo:
                await message.edit_text(text=messg)
            else:
                await message.edit_caption(caption=messg)
        except Exception:
            pass


def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    units = {0: " ", 1: "K", 2: "M", 3: "G", 4: "T"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}B"


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
    )
    return tmp[:-2]


async def upload_thingy(message):
    bc = await bot.send_message(
        chat_id=message.from_user.id,
        text="Downloading The Video",
        reply_to_message_id=message.id,
    )
    d_start = time.time()
    dfix = "➣ **Ꭰᴏwnlᴏᴀding Ꭲhᴇ Ꮩidᴇᴏ** 🚴‍♀️"
    filename = await bot.download_media(
        message,
        progress=progress_for_pyrogram,
        progress_args=(bot, dfix, bc, d_start),
    )
    file_name = os.path.split(filename)[1]
    await bc.edit("Trying To Upload")
    result = await upload(filename, message)
    if result != "Not_Authorised":
        await bc.edit(
            f"File : {file_name}\nHere Is The Download Link [Here]({result})",
            disable_web_page_preview=True,
        )
    else:
        await bc.edit("Upload Failed")


async def add_task(m: Message):
    await upload_thingy(m)
    await on_task_complete()


async def on_task_complete():
    if data:
        del data[0]
    if data:
        await add_task(data[0])
    else:
        data.clear()
