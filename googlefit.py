import os
import httplib2

from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials


class GoogleFit():
	def __init__(self, client_id, client_secret, access_token=None, refresh_token=None):
		self.client_id = client_id
		self.client_secret = client_secret
		self.access_token = access_token
		self.refresh_token = refresh_token
		self.credentials = AccessTokenCredentials(access_token, 'null')
		self.http = httplib2.Http()
		self.http = self.credentials.authorize(self.http)

	def get_points(self, start_time, end_time):
		datasetId = '{}-{}'.format(start_time, end_time)
		service = build('fitness', 'v1', http=self.http)
		request = service.users().dataSources().datasets().get(userId='me', dataSourceId='derived:com.google.step_count.delta:com.google.android.gms:estimated_steps', datasetId=datasetId)
		response = request.execute()
		points = response['point']
		return points
