import httplib2
import os
import base64
import email
import notify2
import math

from apiclient import errors
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'gmail-desktop-notify'
TIMESTAMP = open('prev_time', 'r+')
ICON = '/home/athulp/Downloads/gmail.svg'
EMAIL_ID = 'athul929@gmail.com'
notify2.init('Emails')

def get_credentials():
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir, 'gmail-desktop-notify.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		credentials = tools.run_flow(flow, store)
	return credentials


credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('gmail', 'v1', http=http)


def ListMessagesMatchingQuery(service, user_id, max = 10, query=''):
	response = service.users().messages().list(userId=user_id,maxResults = max,  q=query).execute()
	messages = []
	if 'messages' in response:
	  messages.extend(response['messages'])
	return messages

def GetMessage(service, user_id, msg_id):
	message = service.users().messages().get(userId=user_id, id=msg_id).execute()
	print(TIMESTAMP.read())
	print(type(message['internalDate']))
	notify2.Notification('New message from '+message['payload']['headers'][1]['value'], message['snippet'], ICON ).show()
	if TIMESTAMP.closed is False:
		print('hi')
		TIMESTAMP.write(message['internalDate'])
		TIMESTAMP.close()
	return message

for message in ListMessagesMatchingQuery(service, EMAIL_ID, 1, 'is:unread category:primary'):
	GetMessage(service, EMAIL_ID, message['id'])