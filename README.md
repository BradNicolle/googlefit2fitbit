# googlefit2fitbit
A script to copy Google Fit data across to FitBit. It requires Google Fitness API access and FitBit API access (client ID, client secret, access token, refresh token). It is designed to run in Heroku using the Heroku Scheduler to periodically sync data across. It expects API details to be stored in Heroku config vars (equivalent to environment variables) and updates these by calling the Heroku API when access tokens are refreshed.

Very much still a work in progress!
