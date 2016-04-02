import os
import fitbit
import googlefit
import logging
import time

#logging.basicConfig(level=logging.DEBUG)

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
GOOGLE_ACCESS_TOKEN = os.environ.get('GOOGLE_ACCESS_TOKEN')
GOOGLE_REFRESH_TOKEN = os.environ.get('GOOGLE_REFRESH_TOKEN')

FITBIT_CLIENT_ID = os.environ.get('FITBIT_CLIENT_ID')
FITBIT_CLIENT_SECRET = os.environ.get('FITBIT_CLIENT_SECRET')
FITBIT_ACCESS_TOKEN = os.environ.get('FITBIT_ACCESS_TOKEN')
FITBIT_REFRESH_TOKEN = os.environ.get('FITBIT_REFRESH_TOKEN')

google_client = googlefit.GoogleFit(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, access_token=GOOGLE_ACCESS_TOKEN, refresh_token=GOOGLE_REFRESH_TOKEN)
fitbit_client = fitbit.Fitbit(FITBIT_CLIENT_ID, FITBIT_CLIENT_SECRET, access_token=FITBIT_ACCESS_TOKEN, refresh_token=FITBIT_REFRESH_TOKEN)

now = int(time.time()*1000000000)
start = now - 1000000000*60*60*3
print(google_client.get_points(start, now))

print(fitbit_client.log_activity(data={'activityName': 'running', 'manualCalories': '100', 'startTime': '00:00:00', 'date': '2016-03-01', 'durationMillis': '10000'}))