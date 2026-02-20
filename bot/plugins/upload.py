import os.path as path

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from bot import LOGS, td
from bot.plugins.authorise import check_user, proceed_or_not


async def upload(filename, message):
    check_user(message)
    priority = await proceed_or_not(message)
    if priority == "quit":
        return "Not_Authorised"

    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(str(message.from_user.id))

    if gauth.credentials is None:
        LOGS.info("Missing Google credentials for %s", message.from_user.id)
        return "Not_Authorised"

    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(str(message.from_user.id))
    else:
        gauth.Authorize()

    drive = GoogleDrive(gauth)
    http = drive.auth.Get_Http_Object()

    if not path.exists(filename):
        LOGS.info("Specified filename %s does not exist", filename)
        return "Not_Authorised"

    td_creds = td.find_one({"id": message.from_user.id})
    if not td_creds:
        return "Not_Authorised"

    file_params = {
        "title": filename.split("/")[-1],
        "parents": [
            {
                "kind": "drive#fileLink",
                "teamDriveId": td_creds["TEAMDRIVE_ID"],
                "id": td_creds["TEAMDRIVE_FOLDER_ID"],
            }
        ],
    }

    file_to_upload = drive.CreateFile(file_params)
    file_to_upload.SetContentFile(filename)

    try:
        file_to_upload.Upload(param={"supportsTeamDrives": True, "http": http})
        fileid = file_to_upload["id"]
        return f"https://drive.google.com/file/d/{fileid}/view"
    except Exception as exc:
        LOGS.info(exc)
        return "Not_Authorised"
