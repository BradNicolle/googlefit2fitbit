import requests

class HerokuConfigVars:
	API_ENDPOINT = 'https://api.heroku.com'
	API_ACCEPT = 'application/vnd.heroku+json; version=3'

	def __init__(self, APP_ID, API_KEY):
		self.APP_ID = APP_ID
		self.API_KEY = API_KEY

	def get_request(self, url):
		headers = {'Authorization': 'Bearer ' + self.API_KEY, 'Accept': self.API_ACCEPT}
		return requests.get(self.API_ENDPOINT + url, headers=headers).json()

	def patch_request(self, url, data):
		headers = {'Authorization': 'Bearer ' + self.API_KEY, 'Content-Type': 'application/json', 'Accept': self.API_ACCEPT}
		return requests.patch(self.API_ENDPOINT + url, json=data, headers=headers).json()

	def get_config_vars(self):
		return self.get_request('/apps/{}/config-vars'.format(self.APP_ID))

	def set_config_var(self, key, value):
		config_vars = self.get_config_vars()
		config_vars[key] = value
		print(config_vars)
		return self.patch_request('/apps/{}/config-vars'.format(self.APP_ID), config_vars)
