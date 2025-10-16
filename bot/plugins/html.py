from bot import bot, Config
import os, asyncio, pyrogram
from .authorise import check_user
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth, AuthenticationError
from AnilistPython import Anilist
from .template import html as helium
from .template import remains

anilist = Anilist()

async def html(bot, message):
  ope = open('html.html', 'w')
  msg = await bot.ask(chat_id=message.from_user.id, text="Send Links To Create Html Href And /done To Stop Process")
  ep = 1
  while (msg.text != '/done'):
   ope.write(f'<a href="{msg.text}">Episode {ep}</a>\n')
   ep = ep + 1
   msg = await bot.ask(chat_id=message.from_user.id, text="Send Links To Create Html Href And /done To Stop Process")
  ope.close()
  await bot.send_document(chat_id=message.from_user.id, document='html.html')

async def html2(bot, message):
   data = []
   anime_name = await bot.ask(chat_id=message.from_user.id, text="Enter Anime Name")
   check_user(anime_name)
   season = []
   link = ''
   ## GETTING ANIME INFO REQUIRED
   anime_name = anime_name.text
   dictt = anilist.get_anime(anime_name)
   image = dictt["cover_image"]
   title = dictt["name_english"]
   synopsis = str(dictt["desc"])
   synopsis = synopsis.lower()
   synopsis = synopsis.capitalize()
   ## COMPLETED GETTING ANIME INFO
   msg = await bot.ask(chat_id=message.from_user.id, text="Send Teamdrive Folder ID And /done To Stop Process")
   bcc = await bot.ask(chat_id=message.from_user.id, text="First Episode Number.")
   while msg.text != '/done':
    bcc = int(bcc.text)
    team_drive_id = msg.text
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(str(message.from_user.id))
    drive = GoogleDrive(gauth)
    bc = ''
    file_list = drive.ListFile({'q': f"'{team_drive_id}' in parents and trashed=false", 'includeItemsFromAllDrives': True, 'supportsAllDrives': True}).GetList()
    data.clear()
    print(data)
    for file1 in file_list:
     view_link = f"https://drive.google.com/file/d/{file1['id']}/view"
     data.append(view_link)
    data.reverse()
    ep = bcc
    for i in range(0, len(data)):
      bc = bc + f'<p>📌<a href="{data[i]}" target="_blank">Episode {ep}</a></p>\n'
      ep = ep + 1
    season.append(bc)
    msg = await bot.ask(chat_id=message.from_user.id, text="Send Teamdrive Folder ID And /done To Stop Process")
    bcc = await bot.ask(chat_id=message.from_user.id, text="First Episode Number.")
    data.clear()  
   for x in range(0, len(season)):
     link = link + f'<button class="collapsible">Season {x+1} -:</button>\n<div class="content">\n{season[x]}</div>'
   html = helium.format(image = image, title = title, synopsis = synopsis, link = link)
   html = html + remains
   with open(f'{title}.html', 'w') as results:
     results.write(html)
     results.close()  
   await bot.send_document(chat_id=message.from_user.id, document=f'{title}.html')
   os.remove(f'{title}.html')
   
