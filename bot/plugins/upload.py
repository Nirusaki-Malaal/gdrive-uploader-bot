import json, re, os, sys, pyrogram, subprocess, argparse
import os.path as path
from bot import Creds, LOGS, Config, td
from pydrive.auth import GoogleAuth
from bot.plugins.authorise import check_user, proceed_or_not
from pydrive.drive import GoogleDrive

async def upload(filename, message):
 parent_folder = "Gdrive_Bot"
 drive: GoogleDrive
 FOLDER_MIME_TYPE = 'application/vnd.google-apps.folder'
 http = None
 initial_folder = None
 gauth: drive.GoogleAuth = GoogleAuth()
 check_user(message)
 priority = await proceed_or_not(message)
 if priority == "quit":
   return
 gauth.LoadCredentialsFile(str(message.from_user.id))
 if gauth.credentials is None:
   LOGS.info("NOT AUTH USERS")
 elif gauth.access_token_expired:
  gauth.Refresh() ## # Refresh Them If Expired ##
  gauth.SaveCredentialsFile(str(message.from_user.id))
 else:
  gauth.Authorize() ## Initialize The Saved Credentials ##
  drive = GoogleDrive(gauth)
  http = drive.auth.Get_Http_Object()
  if not path.exists(filename):
   LOGS.info(f"Specified filename {filename} does not exist!")
   return
  file_params = {'title': filename.split('/')[-1]}
  td_creds = td.find_one({'id' : message.from_user.id})
  file_params['parents'] = [{"kind": "drive#fileLink", "teamDriveId": td_creds["TEAMDRIVE_ID"], "id": td_creds["TEAMDRIVE_FOLDER_ID"]}]
  file_to_upload = drive.CreateFile(file_params)
  file_to_upload.SetContentFile(filename)
  try:
      file_to_upload.Upload(param={"supportsTeamDrives" : True, "http" : http})
      lamb = True
      fileid = file_to_upload['id']
      file_link = f"https://drive.google.com/file/d/{fileid}/view"
      return file_link
  except Exception as e:
      LOGS.info(e)
      return "Not_Authorised"


#  if not Creds.TEAMDRIVE_FOLDER_ID:
#    file_to_upload.FetchMetadata()
#   file_to_upload.InsertPermission({'type':  'anyone', 'value': 'anyone', 'role':  'reader', 'withLink': True})
