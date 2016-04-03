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

UTC = tz.gettz('UTC')
LOCAL_TIMEZONE = tz.gettz('Australia/Sydney')

google_client = googlefit.GoogleFit(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, access_token=GOOGLE_ACCESS_TOKEN, refresh_token=GOOGLE_REFRESH_TOKEN)
fitbit_client = fitbit.Fitbit(FITBIT_CLIENT_ID, FITBIT_CLIENT_SECRET, access_token=FITBIT_ACCESS_TOKEN, refresh_token=FITBIT_REFRESH_TOKEN)

now = int(time.time()*1000)
start = now - 1000*60*60*24
buckets = google_client.get_buckets(start, now)

for bucket in buckets:
	for dataset in bucket['dataset']:
		if 'point' in dataset:
			point = dataset['point'][0]
			duration_millis = (int(point['endTimeNanos']) - int(point['startTimeNanos'])) / 1000000
			start_datetime = datetime.utcfromtimestamp(int(point['startTimeNanos']) / 1000000000)
			start_datetime = start_datetime.replace(tzinfo=UTC).astimezone(LOCAL_TIMEZONE)
			start_time = start_datetime.strftime('%H:%M:%S')
			start_date = start_datetime.strftime('%Y-%m-%d')
			distance = point['value'][0]['intVal']
			if distance > 0:
				print("{} {} {} {}".format(start_time, start_date, duration_millis, distance))
				fitbit_client.log_activity(data={'activityId': 90013, 'startTime': start_time, 'date': start_date, 'durationMillis': int(duration_millis), 'distance': distance, 'distanceUnit': 'steps'})
