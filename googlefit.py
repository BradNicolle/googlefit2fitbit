import os
import time
import httplib2

from apiclient.discovery import build
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow

CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, 'https://www.googleapis.com/auth/fitness.activity.read')

storage = Storage('credentials.dat')
credentials = storage.get()

if (credentials is None or credentials.invalid):
	credentials = tools.run_flow(flow, storage, tools.argparser.parse_args())

http = httplib2.Http()
http = credentials.authorize(http)

now = int(time.time()*1000000000)
dayAgo = now - 1000000000*60*60*3
datasetId = '{}-{}'.format(dayAgo, now)
print(datasetId)

service = build('fitness', 'v1', http=http)
request = service.users().dataSources().datasets().get(userId='me', dataSourceId='derived:com.google.step_count.delta:com.google.android.gms:estimated_steps', datasetId=datasetId)
response = request.execute()

points = response['point']

total = 0
for point in points:
	print(point['value'])
	total += point['value'][0]['intVal']

print('TOTAL:')
print(total)
