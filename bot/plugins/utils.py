
import os, math, pyrogram, time
from bot import data, LOGS, bot
from pyrogram.types import Message
from .upload import upload

async def progress_for_pyrogram(current, total, bot, ud_type, message, start):
    now = time.time()
    FINISHED_PROGRESS_STR = "▣"
    UN_FINISHED_PROGRESS_STR = "□"
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
        pro_bar = "{0}{1}".format(''.join([FINISHED_PROGRESS_STR for i in range(math.floor(percentage / 10))]), ''.join([UN_FINISHED_PROGRESS_STR for i in range(10 - math.floor(percentage / 10))]))
        perc_b = '{0}'.format(round(percentage, 2))
        done_mb = '{0}'.format(humanbytes(current))
        total_mb = '{0}'.format(humanbytes(total))
        spid = '{0}'.format(humanbytes(speed))
        messg = f"{ud_type}\n➣ **Ꮲᴇrᴄᴇnᴛ** 🗿 : {perc_b} \n➣ **Ꭲᴏᴛᴀl Ꮪizᴇ** 🎯 : {total_mb}\n➣ **Ꮯᴏʍᴩlᴇᴛᴇd** 🏗 : {done_mb}\n➣ **Ꭲiʍᴇ Ꮮᴇfᴛ** ⌛️ : {estimated_total_time if estimated_total_time != '' else '0 s'}\n➣ **Ꮪᴩᴇᴇd** 🚀 : {spid}\n➢ {pro_bar}"
        try:
         if not message.photo:
          await message.edit_text(text=messg)
         else:
          await message.edit_caption(caption=messg)
        except:
         pass

def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2]

async def upload_thingy(message):
    bc = await bot.send_message(chat_id=message.from_user.id, text="Downloading The Video", reply_to_message_id=message.id)
    d_start = time.time()
    dfix = "➣ **Ꭰᴏwnlᴏᴀding Ꭲhᴇ Ꮩidᴇᴏ** 🚴‍♀️"  
    filename = await bot.download_media(message,progress=progress_for_pyrogram , progress_args=(bot, dfix, bc, d_start))
    file_name = os.path.split(filename)[1]
    await bc.edit("Trying To Upload")
    bcc = await upload(filename, message)
    if not bcc == 'Not_Authorised':
      await bc.edit(f"File : {file_name}\nHere Is The Download Link [Here]({bcc})", disable_web_page_preview=True)
    else:
      await bc.edit("Upload Failed")

async def add_task(m: Message):
    await upload_thingy(m)
    await on_task_complete()

async def on_task_complete():
    del data[0]
    if len(data) > 0:
      await add_task(data[0])
    else:
     data.clear()
