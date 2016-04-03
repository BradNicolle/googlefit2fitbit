import os
import httplib2

from apiclient.discovery import build
from oauth2client.client import GoogleCredentials
from oauth2client import GOOGLE_TOKEN_URI
from datetime import datetime
from dateutil import tz

UTC = tz.gettz('UTC')

class StepData:
	def __init__(self, start_time, start_date, duration_millis, steps):
		self.start_time = start_time
		self.start_date = start_date
		self.duration_millis = duration_millis
		self.steps = steps


class GoogleFit():
	def __init__(self, client_id, client_secret, access_token=None, refresh_token=None):
		self.client_id = client_id
		self.client_secret = client_secret
		self.access_token = access_token
		self.refresh_token = refresh_token
		self.credentials = GoogleCredentials(access_token, client_id, client_secret, refresh_token, None, GOOGLE_TOKEN_URI, 'googlefit2fitbit', None)
		self.http = httplib2.Http()
		self.http = self.credentials.authorize(self.http)

	def get_buckets(self, start_timestamp, end_timestamp):
		service = build('fitness', 'v1', http=self.http)
		request = service.users().dataset().aggregate(userId='me', body={'aggregateBy': [{'dataSourceId':'derived:com.google.step_count.delta:com.google.android.gms:estimated_steps'}], 'startTimeMillis': start_timestamp, 'endTimeMillis': end_timestamp, 'bucketByTime': {'durationMillis': 3600000}})
		response = request.execute()
		buckets = response['bucket']
		return buckets

	def get_steps(self, start_timestamp, end_timestamp, local_timezone):
		buckets = self.get_buckets(start_timestamp, end_timestamp)
		step_points = []
		for bucket in buckets:
			for dataset in bucket['dataset']:
				if 'point' in dataset:
					point = dataset['point'][0]

					duration_millis = (int(point['endTimeNanos']) - int(point['startTimeNanos'])) / 1000000
					start_datetime = datetime.utcfromtimestamp(int(point['startTimeNanos']) / 1000000000)
					start_datetime = start_datetime.replace(tzinfo=UTC).astimezone(local_timezone)
					
					start_time = start_datetime.strftime('%H:%M:%S')
					start_date = start_datetime.strftime('%Y-%m-%d')
					distance = point['value'][0]['intVal']

					step_data = StepData(start_time, start_date, int(duration_millis), distance)
					step_points.append(step_data)
		return step_points
