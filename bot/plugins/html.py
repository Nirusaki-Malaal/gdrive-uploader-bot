import os
import re

from AnilistPython import Anilist
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from .authorise import check_user
from .template import html as helium
from .template import remains

anilist = Anilist()


async def html(bot, message):
    with open("html.html", "w", encoding="utf-8") as output:
        msg = await bot.ask(
            chat_id=message.from_user.id,
            text="Send links to create HTML href entries and /done to stop",
        )
        ep = 1
        while msg.text != "/done":
            output.write(f'<a href="{msg.text}">Episode {ep}</a>\n')
            ep += 1
            msg = await bot.ask(
                chat_id=message.from_user.id,
                text="Send links to create HTML href entries and /done to stop",
            )

    await bot.send_document(chat_id=message.from_user.id, document="html.html")


async def html2(bot, message):
    season_blocks = []
    anime_name_msg = await bot.ask(chat_id=message.from_user.id, text="Enter Anime Name")
    check_user(message)

    anime_name = anime_name_msg.text
    anime = anilist.get_anime(anime_name)
    image = anime["cover_image"]
    title = anime.get("name_english") or anime.get("name_romaji") or anime_name
    synopsis = str(anime["desc"]).lower().capitalize()

    msg = await bot.ask(
        chat_id=message.from_user.id,
        text="Send Team Drive folder ID and /done to stop process",
    )
    first_ep_msg = await bot.ask(chat_id=message.from_user.id, text="First episode number")

    while msg.text != "/done":
        first_ep = int(first_ep_msg.text)
        team_drive_id = msg.text

        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(str(message.from_user.id))
        drive = GoogleDrive(gauth)

        file_list = drive.ListFile(
            {
                "q": f"'{team_drive_id}' in parents and trashed=false",
                "includeItemsFromAllDrives": True,
                "supportsAllDrives": True,
            }
        ).GetList()

        links = [f"https://drive.google.com/file/d/{item['id']}/view" for item in file_list]
        links.reverse()

        current_ep = first_ep
        block = ""
        for link in links:
            block += f'<p>📌<a href="{link}" target="_blank">Episode {current_ep}</a></p>\n'
            current_ep += 1

        season_blocks.append(block)
        msg = await bot.ask(
            chat_id=message.from_user.id,
            text="Send Team Drive folder ID and /done to stop process",
        )
        first_ep_msg = await bot.ask(chat_id=message.from_user.id, text="First episode number")

    collapsible_links = "".join(
        f'<button class="collapsible">Season {index + 1} -:</button>\n'
        f'<div class="content">\n{season}</div>'
        for index, season in enumerate(season_blocks)
    )

    html_content = helium.format(
        image=image,
        title=title,
        synopsis=synopsis,
        link=collapsible_links,
    ) + remains

    safe_title = re.sub(r"[^A-Za-z0-9._-]+", "_", title).strip("_") or "anime"
    output_file = f"{safe_title}.html"
    with open(output_file, "w", encoding="utf-8") as result:
        result.write(html_content)

    await bot.send_document(chat_id=message.from_user.id, document=output_file)
    os.remove(output_file)
