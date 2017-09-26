# Google Analytics Reporting API v4 in Python with pandas
This repo contains a setup to get started with the Google Analytics Reporting API v4 in Python. It takes three steps:

# 1. Created a project
First, create a project in your Google Developer console. I highly recommend using [the 17 steps of this post](https://www.themarketingtechnologist.co/google-oauth-2-enable-your-application-to-access-data-from-a-google-user/). Fill out the `client_id`, `client_secret` and `redirect_uri` in the `config.py` file. 

# 2. Connect to the API
To connect to the Google Analytics API, run `config.py` two times:

1. Your first run prints a URL in the console. Open the URL, grant access to your Google account of choice, and copy the `&code=` parameter value and set it as the `access_code` variable.
2. Your second run prints the access token and refresh token. Copy both values and set them as the `access_token` and `refresh_token` variables.

All future runs will use the access token and refresh token to connect to the API.

# 3. Run your report.
Lastly, you can run your reports. The `return_ga_data` function returns a [pandas](http://pandas.pydata.org/) DataFarme. The example code is set to return sessions by source:

```python
df = return_ga_data(
  start_date='2017-09-13',
  end_date='2017-09-21',
  view_id='100555616',
  metrics=[{'expression': 'ga:sessions'},],
  dimensions=[{'name': 'ga:source'}],
  split_dates=False,
  group_by=[]
)
```
A brief description of each parameter:

- `start_date` & `end_date`:
 - date format in `'YYYY-MM-DD'`
 - relative date: `'today'`, `'yesterday'`, `'NdaysAgo'` (where N is the amount of days)
- `view_id`: the ID of the Google Analytics view you want to import data from.
- `metrics`: the list of sessions you want to import (max. 10) - full list [here](https://developers.google.com/analytics/devguides/reporting/core/dimsmets).
- `dimensions`: the list of dimensions you want to import (max. 9) - full list [here](https://developers.google.com/analytics/devguides/reporting/core/dimsmets).
- `split_dates`: boolean. If true each day in your date range is queries seperately and merged into a data frame later on.
- `group_by` (optional): if you enable `split_dates` you can group the data on a dimension of choice. Especially handy when you're not include the date in your export. 
