import os
import fitbit
import googlefit
import logging
import time
from datetime import datetime
from dateutil import tz

logging.basicConfig(level=logging.DEBUG)

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
GOOGLE_ACCESS_TOKEN = os.environ.get('GOOGLE_ACCESS_TOKEN')
GOOGLE_REFRESH_TOKEN = os.environ.get('GOOGLE_REFRESH_TOKEN')

FITBIT_CLIENT_ID = os.environ.get('FITBIT_CLIENT_ID')
FITBIT_CLIENT_SECRET = os.environ.get('FITBIT_CLIENT_SECRET')
FITBIT_ACCESS_TOKEN = os.environ.get('FITBIT_ACCESS_TOKEN')
FITBIT_REFRESH_TOKEN = os.environ.get('FITBIT_REFRESH_TOKEN')


LOCAL_TIMEZONE = tz.gettz('Australia/Sydney')

#google_client = googlefit.GoogleFit(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, access_token=GOOGLE_ACCESS_TOKEN, refresh_token=GOOGLE_REFRESH_TOKEN)
fitbit_client = fitbit.Fitbit(FITBIT_CLIENT_ID, FITBIT_CLIENT_SECRET, access_token=FITBIT_ACCESS_TOKEN, refresh_token=FITBIT_REFRESH_TOKEN)
fitbit_client.client.refresh_token()
print(fitbit_client.client.token)
print(fitbit_client.user_profile_get())
sys.exit()

now = int(time.time()*1000)
start = now - 1000*60*60*24
step_points = google_client.get_steps(start, now, LOCAL_TIMEZONE)

for point in step_points:
	if point.distance > 0:
		print("{} {} {} {}".format(point.start_time, point.start_date, point.duration_millis, point.steps))
		fitbit_client.log_activity(data = { 'activityId': 90013,
											'startTime': point.start_time,
											'date': point.start_date,
											'durationMillis': point.duration_millis,
											'distance': point.steps,
											'distanceUnit': 'steps' })
