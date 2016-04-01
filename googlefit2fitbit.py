import os
import fitbit

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
REFRESH_TOKEN = os.environ.get('REFRESH_TOKEN')

authd_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

print(authd_client.log_activity(data={'activityName': 'running', 'manualCalories': '100', 'startTime': '00:00:00', 'date': '2016-03-01', 'durationMillis': '10000'}))