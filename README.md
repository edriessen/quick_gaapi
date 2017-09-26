# Google Analytics Reporting API v4 in Python with pandas
This repo contains a setup to get started with the Google Analytics Reporting API v4 in Python. It takes three steps:

# 1. Create a project
First, create a project in your Google Developer console. I highly recommend using [the 17 steps of this post](https://www.themarketingtechnologist.co/google-oauth-2-enable-your-application-to-access-data-from-a-google-user/). Add a `credentials.py` file to your Python project and create variables for the `client_id`, `client_secret` and `redirect_uri` and fill out the corresponding values.

*For your Python project, I recommend using Python 3.x over 2.7 because it's better and handling special characters in strings.*

# 2. Connect to the API
To connect to the Google Analytics API, run `config.py` two times:

1. Your first run prints a URL in the console. Open the URL, grant access to your Google account of choice, copy the `&code=` parameter value and add an `access_code` variable with the parameter value in `credentials.py`.
2. Your second run prints the access token and refresh token. For both values, create a variable (`access_token` and `refresh_token`) and set the corresponding values.
 - the refresh token is only returned with your first API connection. If the second line says `None`, revoke your app's access at https://myaccount.google.com/permissions, clear the `access_code` and reconnect.

All future runs will use the access token and refresh token to connect to the API.

# 3. Run your report.
Lastly, you can run `run.py` to return a report in a DataFrame. The `return_ga_data` function returns a [pandas](http://pandas.pydata.org/) DataFarme. The example code is set to return sessions by source:

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

**To do**
The next steps are:

- Add support for segments.
- Add support for dimensionFilterClauses.

